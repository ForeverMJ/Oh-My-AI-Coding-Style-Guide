# Oh-My-AI-Coding-Style-Guide

`Oh-My-AI-Coding-Style-Guide` は、コーディングエージェント向けの公開可能なコンテキスト最適化スキルプロジェクトです。

本リポジトリには以下が含まれます：

- スキルの振る舞い契約
- 実装向けスキル仕様
- ホスト非依存の `SKILL.md` スキル本体
- 評価計画とテストレポート
- OpenCode、Claude Code、Codex 用のワンコマンドインストーラー

## プロジェクトが解決する課題

このスキルは、エージェントが以下のような環境で効率的に動作できるようにします：

- コンテキストウィンドウが限られている
- トークンコストが実質的に発生する
- ツールの可用性が不確実
- リポジトリの内容が疎である

コア動作原則：

- 広範な展開よりも検索を優先
- 全量読み込みよりも選択を優先
- 過早な圧縮よりも要約を優先
- プロンプトのみのフォールバックモードでも有用性を維持

## ワンコマンドインストール

### Claude Code

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude
```

### OpenCode

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode
```

### Codex

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target codex
```

### プロジェクトローカルインストール（ユーザーグローバルではなく）

```bash
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target claude --scope project
```

### ターゲット自動検出

ターゲットプロジェクトにサポート対象のホストディレクトリが1つだけ含まれている場合、自動検出が使用できます：

```bash
python3 install.py --target auto --scope project
```

## インストール内容

インストーラーはスキル本体と付属の原則ファイルを各ホストのスキルディレクトリに書き込みます：

- **Claude Code**
  - ユーザー：`~/.claude/skills/context-optimization/SKILL.md`
  - プロジェクト：`.claude/skills/context-optimization/SKILL.md`

- **OpenCode**
  - ユーザー：`~/.config/opencode/skills/context-optimization/SKILL.md`
  - プロジェクト：`.opencode/skills/context-optimization/SKILL.md`

- **Codex**
  - ユーザー：`~/.agents/skills/context-optimization/SKILL.md`
  - プロジェクト：`.agents/skills/context-optimization/SKILL.md`

付属の `principles.md`（コンテキスト最適化ルールの要約版）は `SKILL.md` と同じディレクトリに常にインストールされます。

`--scope project` と `--init-always-on` を併用すると、インストーラーはこれらの原則をホストの常駐プロンプトメカニズムに追加注入します：

- **OpenCode (oh-my-openagent)**：`prompt_append` で `principles.md` を指定する `.opencode/oh-my-openagent.jsonc` を作成
- **Claude Code**：`CLAUDE.md` に原則を追記
- **Codex**：`AGENTS.md` に原則を追記

## 常駐コンテキスト規律

`--init-always-on` フラグは、コンテキスト最適化原則をホストの主エージェントに対して**常に有効**にし、スキルの明示的な呼び出しを不要にします。トークン予算意識と検索規律をすべての対話で実現したいユーザーに推奨します。

```bash
# プロジェクトスコープの常駐注入
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --scope project --init-always-on

# ユーザーグローバルインストール
curl -fsSL https://raw.githubusercontent.com/ForeverMJ/Oh-My-AI-Coding-Style-Guide/main/install.py | python3 - --target opencode --init-always-on
```

各ホストの常駐注入メカニズム：

| ホスト | 常駐メカニズム | 書き込みファイル |
|---|---|---|
| OpenCode | oh-my-openagent `prompt_append` | `.opencode/oh-my-openagent.jsonc` |
| Claude Code | `CLAUDE.md` 自動注入 | `CLAUDE.md` |
| Codex | `AGENTS.md` 自動注入 | `AGENTS.md` |

## インストーラーの安全な動作

インストーラーは以下をサポート：

- `--dry-run` 書き込みプレビュー
- `--force` 既存の異なるファイルを上書き
- `--scope user|project`
- `--target auto|claude|opencode|codex`
- `--init-always-on` コンテキスト最適化原則をホストの常駐プロンプトファイルに注入

例：

```bash
python3 install.py --target opencode --dry-run
python3 install.py --target claude --scope project
python3 install.py --target codex --force
```

## Codex に関する注意

Codex は `AGENTS.md` に常駐リポジトリガイダンスが存在する場合に最も効果的です。

本リポジトリにはオプションのスニペットが含まれています：

```text
snippets/CODEX_AGENTS_SNIPPET.md
```

スニペットを直接表示：

```bash
python3 install.py --print-codex-agents-snippet
```

## ローカル検証

インストーラーのテスト実行：

```bash
python3 -m unittest tests/test_install.py
```

ドライラン：

```bash
python3 install.py --target claude --dry-run
```

## リポジトリファイル

- `DESIGN.md` — 振る舞い契約
- `SKILL_SPEC.md` — 実装向けスキル仕様
- `SKILL.md` — ホスト非依存のスキル本体（ソースファイル）
- `EVALUATION.md` — テスト計画
- `TEST_REPORT.md` — 評価結果記録
- `install.py` — ワンコマンドインストーラー

## 評価結果

このスキルは `EVALUATION.md` のテスト計画に従って評価されました。結果は `TEST_REPORT.md` に記録されています。主な発見：

- **総合：合格。** スキルの振る舞いは3つの動作モード（tool-assisted、prompt-only、partial-tools）でいずれも信頼性があります。
- **第1ラウンドの8つのコアテストケースがすべて合格**し、モード正しさ、グレースフルデグラデーション、疎リポジトリ規律、捏造防止をカバー。
- **第2ラウンドの回帰テスト**で、出力列挙の厳密化（`Mode Used` と `Evidence Level` を厳密な列挙型に）がコア動作を壊さずに一貫性を向上させることを確認。
- **実用性テスト**では、スキルは疎リポジトリで明確な勝利を示し（より良いコンテキスト規律、より少ないトークン）、中規模リポジトリでも振る舞い統治層として有用。ただし生のトークン節約は限界的でした。
- スキルの最大の価値は**コンテキスト規律とスコープ制御**であり、生の効率の保証ではありません。

詳細な結果、トレーサビリティマトリクス、合格基準は `TEST_REPORT.md` を参照。

## トークン節約の定量化

`opencode` リポジトリ（52,218ソースファイル）でCodexを使用し、常駐原則注入の有無によるトークン使用量を比較する定量化テストを実施しました。6つの異なる複雑度のタスクを実行しました。

### テスト結果

| タスク | ベースライン | スキル使用 | 削減 |
|---|---|---|---|
| T1：skill読み込みファイル特定 | 187,766 | 162,846 | **-13.3%** |
| T2：テストファイル数の集計 | 26,248 | 18,342 | **-30.1%** |
| T3：テストコマンドの検索 | 17,105 | 17,769 | -3.9% |
| T4：設定読み込みロジック | タイムアウト | 387,750 | *スキル完了* |
| T5：MCPファイルの一覧 | 142,849 | 91,391 | **-36.0%** |
| T6：ビルドツールチェーンの分析 | タイムアウト | 434,018 | *スキル完了* |
| **合計** | **373,968** | **290,348** | **-22.4%** |

### 主な発見

- **平均トークン削減：22.4%**
- **ファイル探索タスク**（T1、T5）の効果が最も大きく、13-36%の節約。
- **簡単な設定クエリ**（T3）では差異が最小。
- **複雑なタスク**（T4、T6）はスキルなしでタイムアウトしましたが、スキル使用時に成功。スキルがトークン効率に加えてタスク完了の信頼性も向上させることを示唆。
- スキルの主な価値は**コンテキスト規律**にあり、大規模リポジトリでの過剰探索を防ぎつつ回答品質を維持します。

## プロジェクトの共有

最もシンプルなリリースフロー：

1. 本リポジトリを公開
2. `install.py` をデフォルトブランチで利用可能な状態に維持
3. ユーザーにターゲットホストのワンラインインストールコマンドを実行してもらう
