#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiki Harness 기계 검증 스크립트

검증 항목:
1. Frontmatter 검증 (필수 필드)
2. 스키마 구조 검증 (섹션, 필드)
3. 파일명 규칙 검증
4. 출처 링크 검증 ([[YYYY-MM-DD]])
5. ID 형식 검증 (D-XXXX, A-XXXX)
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# UTF-8 인코딩 설정
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ValidationError:
    def __init__(self, file_path: str, error_type: str, message: str):
        self.file_path = file_path
        self.error_type = error_type
        self.message = message

    def __str__(self):
        return f"[{self.error_type}] {self.file_path}: {self.message}"

class WikiValidator:
    def __init__(self, wiki_root: str):
        self.wiki_root = Path(wiki_root)
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    # ===== 기본 검증 =====

    def validate_frontmatter(self, file_path: Path) -> Dict[str, str]:
        """Frontmatter 검증 및 추출"""
        content = file_path.read_text(encoding='utf-8')

        if not content.startswith('---'):
            self.errors.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "FRONTMATTER",
                "파일이 ---로 시작하지 않음"
            ))
            return {}

        # Frontmatter 추출
        end_idx = content.find('---', 3)
        if end_idx == -1:
            self.errors.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "FRONTMATTER",
                "Frontmatter가 닫히지 않음 (---이 없음)"
            ))
            return {}

        frontmatter = content[3:end_idx].strip()
        metadata = {}

        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        return metadata

    def validate_source_links(self, file_path: Path, content: str):
        """출처 링크([[YYYY-MM-DD]]) 검증"""
        # 메타데이터 행이나 헤더는 제외
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # 메타데이터, 헤더, 테이블 헤더는 제외
            if (line.startswith('**') and line.endswith('**') or
                line.startswith('#') or
                '|' in line and '---' in lines[i] if i < len(lines) else False):
                continue

            # 실제 컨텐츠 (bullet point, 텍스트)에서 출처 링크 확인
            if (line.strip().startswith('-') or
                line.strip().startswith('•') or
                (line.strip() and not line.startswith((' ', '\t', '|', '`', '>', '#')))):

                if re.search(r'\[\[(\d{4}-\d{2}-\d{2})\]\]', line):
                    continue  # 출처 링크 있음
                elif line.strip() and len(line.strip()) > 10:  # 충분히 긴 텍스트
                    self.warnings.append(ValidationError(
                        str(file_path.relative_to(self.wiki_root)),
                        "SOURCE_LINK",
                        f"Line {i}: 출처 링크 누락 가능: {line.strip()[:50]}"
                    ))

    def validate_filename(self, file_path: Path, expected_pattern: str = None):
        """파일명 규칙 검증"""
        filename = file_path.name
        parent_dir = file_path.parent.name

        if parent_dir == 'decisions':
            # D-XXXX-제목.md
            if not re.match(r'^D-\d{4}-.+\.md$', filename):
                self.errors.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "FILENAME",
                    f"결정 파일명 규칙 위반: {filename} (예: D-0001-제목.md)"
                ))

        elif parent_dir == 'meetings':
            if filename in ['decisions.md', 'actions.md', 'glossary.md', 'index.md', 'log.md', 'open-items.md']:
                return  # 메타 파일

            # YYYY-MM-DD-제목.md
            if not re.match(r'^\d{4}-\d{2}-\d{2}-.+\.md$', filename):
                self.errors.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "FILENAME",
                    f"회의록 파일명 규칙 위반: {filename} (예: 2026-03-12-회의명.md)"
                ))

    # ===== D 파일 검증 =====

    def validate_decision_file(self, file_path: Path):
        """D-XXXX 파일 검증"""
        content = file_path.read_text(encoding='utf-8')

        # 헤더 검증
        if not re.match(r'^# D-\d{4}:', content):
            self.errors.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "D_FORMAT",
                "헤더 형식 오류: # D-XXXX: 제목"
            ))

        # 필수 섹션 확인
        required_sections = [
            '## 결정 내용',
            '## 검토한 대안',
            '## 근거',
            '## 수정 기록'
        ]

        for section in required_sections:
            if section not in content:
                self.errors.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "D_SECTION",
                    f"필수 섹션 누락: {section}"
                ))

        # 메타데이터 확인
        metadata_fields = ['상태', '담당', '출처']
        for field in metadata_fields:
            if f'**{field}**:' not in content:
                self.errors.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "D_METADATA",
                    f"필수 메타데이터 누락: **{field}**:"
                ))

        # 출처 링크 검증
        self.validate_source_links(file_path, content)

    # ===== Actions.md 검증 =====

    def validate_actions_file(self, file_path: Path):
        """actions.md 검증"""
        content = file_path.read_text(encoding='utf-8')

        # 헤더 확인
        if '# 액션아이템' not in content and '# 액션' not in content:
            self.warnings.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "ACTIONS_FORMAT",
                "예상 헤더 누락: # 액션아이템"
            ))

        # A-XXXX 항목 검증
        action_pattern = r'^### A-(\d{4}):'
        for i, line in enumerate(content.split('\n'), 1):
            match = re.match(action_pattern, line)
            if match:
                action_id = match.group(1)
                # 해당 액션의 메타데이터 검증
                section_end = content.find('###', content.find(line) + 1)
                if section_end == -1:
                    section_end = len(content)

                section = content[content.find(line):section_end]
                required = ['담당', '기한', '상태', '출처']
                for req in required:
                    if f'**{req}**:' not in section:
                        self.errors.append(ValidationError(
                            str(file_path.relative_to(self.wiki_root)),
                            "ACTION_METADATA",
                            f"A-{action_id}: 필수 메타데이터 누락: **{req}**:"
                        ))

    # ===== Index.md 검증 =====

    def validate_index_file(self, file_path: Path):
        """index.md 검증"""
        content = file_path.read_text(encoding='utf-8')

        # 상태 섹션 확인
        required_status = [
            '마지막 할당된 D 번호',
            '마지막 할당된 A 번호',
            '마지막 할당된 용어 건수'
        ]

        for status in required_status:
            if status not in content:
                self.errors.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "INDEX_STATUS",
                    f"상태 항목 누락: {status}"
                ))

        # D/A 번호 형식 검증
        d_match = re.search(r'마지막 할당된 D 번호.*?D-(\d{4})', content)
        a_match = re.search(r'마지막 할당된 A 번호.*?A-(\d{4})', content)

        if not d_match:
            self.errors.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "INDEX_FORMAT",
                "마지막 D 번호 형식 오류: D-XXXX 형식 필요"
            ))

        if not a_match:
            self.errors.append(ValidationError(
                str(file_path.relative_to(self.wiki_root)),
                "INDEX_FORMAT",
                "마지막 A 번호 형식 오류: A-XXXX 형식 필요"
            ))

    # ===== Glossary.md 검증 =====

    def validate_glossary_file(self, file_path: Path):
        """glossary.md 검증"""
        content = file_path.read_text(encoding='utf-8')

        # 섹션 확인
        sections = ['## 약어', '## 팀 시스템명', '## 팀 용어']

        for section in sections:
            if section not in content:
                self.warnings.append(ValidationError(
                    str(file_path.relative_to(self.wiki_root)),
                    "GLOSSARY_SECTION",
                    f"예상 섹션 없음: {section}"
                ))

    # ===== 메인 검증 =====

    def validate_all(self):
        """전체 wiki 검증"""
        print("🔍 Wiki Harness 기계 검증 시작...\n")

        # 1. Decisions 폴더 검증
        decisions_dir = self.wiki_root / 'decisions'
        if decisions_dir.exists():
            print("📋 결정 파일 검증 중...")
            for d_file in decisions_dir.glob('D-*.md'):
                self.validate_filename(d_file)
                self.validate_decision_file(d_file)

        # 2. Meetings 폴더 검증
        meetings_dir = self.wiki_root / 'meetings'
        if meetings_dir.exists():
            print("📅 회의록 검증 중...")

            # 회의록 파일
            for meeting_file in meetings_dir.glob('[0-9]*.md'):
                self.validate_filename(meeting_file)

            # 메타 파일
            actions_file = meetings_dir / 'actions.md'
            if actions_file.exists():
                print("✅ actions.md 검증 중...")
                self.validate_actions_file(actions_file)

            index_file = meetings_dir / 'index.md'
            if index_file.exists():
                print("✅ index.md 검증 중...")
                self.validate_index_file(index_file)

            glossary_file = meetings_dir / 'glossary.md'
            if glossary_file.exists():
                print("✅ glossary.md 검증 중...")
                self.validate_glossary_file(glossary_file)

        self.print_results()

    def print_results(self):
        """검증 결과 출력"""
        print("\n" + "="*60)
        print("🔍 검증 결과")
        print("="*60)

        if not self.errors and not self.warnings:
            print("\n✅ 모든 검증 통과! (오류 없음)")
            return

        if self.errors:
            print(f"\n❌ 오류 {len(self.errors)}개:\n")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print(f"\n⚠️  경고 {len(self.warnings)}개:\n")
            for warning in self.warnings:
                print(f"  {warning}")

        print("\n" + "="*60)

        if self.errors:
            sys.exit(1)
        else:
            sys.exit(0)

def main():
    wiki_root = Path(__file__).parent.parent / 'wiki'

    if not wiki_root.exists():
        print(f"❌ Wiki 디렉토리 없음: {wiki_root}")
        sys.exit(1)

    validator = WikiValidator(wiki_root)
    validator.validate_all()

if __name__ == '__main__':
    main()
