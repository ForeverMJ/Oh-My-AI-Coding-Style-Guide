# Oh-My-AI-Coding-Style-Guide

コーディングエージェント向けのコンテキスト最適化スキル。エージェントが最小限のコンテキストで動作し、過剰な探索を避け、知っていることと推測していることを正直に区別できるようにします。

## 解決する課題

コーディングエージェントがトークンを浪費する一般的な原因：

- 数ファイルしか必要ないのにリポジトリ全体を読み込む
- 「包括的に見える」ために広範に探索する
- 十分なコンテキストがあるのに読み続ける
- 検証済みの事実と推測を区別できない

このスキルは一連の原則を提供し、エージェントの探索動作を制約して、回答品質を維持しながらトークン消費を削減します。

## インストール方法

### 方法1：オンデマンドスキル（デフォルト）

スキルをホストのスキルディレクトリにインストールします。エージェントがマッチするシナリオを認識したとき、ホストのネイティブスキル発見メカニズムを通じてオンデマンドで読み込みます。

```bash
# Codex
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex

# Claude Code
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude

# OpenCode
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode
```

### 方法2：常駐原則（推奨）

コンテキスト最適化原則の要約版をホストの常駐プロンプトファイルに注入します。エージェントはフルスキルを読み込むことなく、すべての対話でこれらの原則に自動的に従います。

```bash
# Codex（AGENTS.md に注入）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex --scope project --init-always-on

# Claude Code（CLAUDE.md に注入）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project --init-always-on

# OpenCode（prompt_append を設定した oh-my-openagent.jsonc を作成）
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --scope project --init-always-on
```

### 2つの方法の違い

| インストール方法 | 内容 | エージェントの動作 |
|---|---|---|
| デフォルト | スキルファイルをスキルディレクトリにインストール | マッチするシナリオを認識したときにオンデマンドで読み込み |
| 常駐原則 | 要約版原則をホストプロンプトに注入 | すべての対話で原則に自動的に従う |

## テスト結果

### 振る舞い評価

異なるサイズのリポジトリで、3つの動作モード（tool-assisted、prompt-only、partial-tools）をテスト：

- **8つのコアテストケースすべて合格** — モード正しさ、グレースフルデグラデーション、疎リポジトリ規律、捏造防止
- **出力契約の安定性** — tool-assisted と prompt-only モードで同じ振る舞い構造
- **捏造なし** — スキルはファイル、モジュール、ツール出力を偽造しない

詳細な結果：`TEST_REPORT.md`

### トークン節約の定量化

`opencode` リポジトリ（52,218ソースファイル）でCodexを使用し、常駐原則の有無によるトークン使用量を比較：

| タスク | ベースライン | スキル使用 | 削減 |
|---|---|---|---|
| T1：skill読み込みファイル特定 | 187,766 | 162,846 | **-13.3%** |
| T2：テストファイル数の集計 | 26,248 | 18,342 | **-30.1%** |
| T3：テストコマンドの検索 | 17,105 | 17,769 | -3.9% |
| T4：設定読み込みロジック | タイムアウト | 387,750 | *スキル完了* |
| T5：MCPファイルの一覧 | 142,849 | 91,391 | **-36.0%** |
| T6：ビルドツールチェーンの分析 | タイムアウト | 434,018 | *スキル完了* |
| **合計** | **373,968** | **290,348** | **-22.4%** |

主な発見：

- **平均トークン削減：22.4%**
- ファイル探索タスクの効果が最も大きい（13-36%の節約）
- スキルなしでタイムアウトした複雑なタスクが、スキル使用時に成功
- スキルの主な価値は**コンテキスト規律**：大規模リポジトリでの過剰探索を防ぎつつ回答品質を維持

## リポジトリファイル

| ファイル | 用途 |
|---|---|
| `SKILL.md` | ホスト非依存のスキル本体（ソースファイル） |
| `DESIGN.md` | 振る舞い契約と受入声明 |
| `SKILL_SPEC.md` | 実装向け仕様 |
| `EVALUATION.md` | テスト計画 |
| `TEST_REPORT.md` | 評価結果 |
| `install.py` | ワンコマンドインストーラー |
| `tests/test_install.py` | インストーラーのテスト |
| `tests/test_quantitative.py` | トークン定量化テストスクリプト |

## ローカル検証

```bash
# インストーラーのテスト実行
python3 -m unittest tests/test_install.py

# ドライラン（プレビュー、ファイル書き込みなし）
python3 install.py --target codex --scope project --init-always-on --dry-run
```
