# Lecture 02 Answers

## Exercises

- Model and settings used (from `config` in `result.json`):
- Did you run training yourself (`executed_training_myself`): Yes / No (how far you ran the notebook: )
- Before training: `format_rate` = / `content_rate` =
- After training: `format_rate` = / `content_rate` =
- Questions that regressed:
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
- Results of knowledge questions (section 6; classification before → after training) and observations:
- What changed and what stayed the same with training:

## Homework

- Level attempted: Basic 
- Settings or data changed:num_train_epochs 20→5 
- Results (comparison tables or numbers):内容の正解数は、学習前の8問から、5エポックで15問、
20エポックで19問に増えた。
- Discussion of when fine-tuning is and is not suitable:
ファインチューニングは、決まった回答形式や振る舞いを
学習させる用途に適していると考えた。
一方、最新情報やFAQにない情報の正確さを保証する用途では、
資料の検索や人による確認なども組み合わせる必要がある。

# Lecture 02 宿題：LoRAの学習回数による比較

## 取り組んだ課題
基礎課題に取り組み、num_train_epochsを20から5に変更して、
学習後の回答形式・内容の正確さ・学習時間を比較した。
両条件とも自分で学習を実行した。

executed_training_myself: True

## 実験方法
配布ノートブックをGoogle Colabで実行した。
モデルはQwen/Qwen3.5-0.8B、学習方法はLoRAを使用した。
学習データは配布された架空の講座FAQを使用し、
変更する設定はnum_train_epochsのみとした。

20エポックで実行した後、セッションを再起動し、
5エポックの条件で最初から実行し直した。

評価では、JSON形式を守れているかを示すformat_rateと、
回答内容・needs_reviewが期待どおりかを示すcontent_rateを比較した。

## 結果

| 条件 | format_rate | content_rate | 最後に記録されたTraining Loss | 学習時間 | ステップ数 |
|---|---:|---:|---:|---:|---:|
| 学習前（両条件共通） | 0.952381 | 0.380952 | — | — | — |
| 20エポック後 | 1.000000 | 0.904762 | 0.014660 | 184秒 | 40 |
| 5エポック後 | 1.000000 | 0.714286 | 1.709299 | 44秒 | 10 |

評価対象は21問だった。
形式を守れた質問数は、学習前の20問から、両条件とも21問に増えた。
内容の正解数は、学習前の8問から、5エポックで15問、
20エポックで19問に増えた。

5エポックでは20エポックに比べ、学習時間が約76％短くなった。
一方、内容の正解数は4問少なかった。
なお、表のlossは最後にログに表示されたTraining Lossであり、
評価時の誤差や学習全体の平均値とは区別している。

## 5エポック後の回答の確認

### 改善した点
FAQに根拠がある15問は、学習後にすべて正解した。
例えば、提出先の質問では、学習前に欠けていたneeds_reviewが
追加され、回答内容と確認要否が正しくなった。

### 根拠のない断言
追加の確認では、FAQにない「最終課題の締切」を尋ねると、
通常の課題の締切を流用し、needs_reviewをfalseとして回答した。
既存のFAQに似た質問に対し、その情報を誤って当てはめていた。

一方、「講師の名前」「次回講義の内容」には、
FAQに記載がないと答え、needs_reviewをtrueにできていた。
未知の情報への対応は、質問によって異なっていた。

### 学習後に悪化した例
Regressionsには「When will grades be released?」が含まれていた。
学習前は「Confirmation is needed」と答え、
needs_reviewをtrueにしていたが、学習後はFAQにない
「October 31 at 23:59」という日時を断言した。

### 自動評価の注意点
「課題に文字数制限はあるか」という質問では、
FAQに記載がないと回答し、needs_reviewをtrueにしていたが、
自動評価では内容が不正解となっていた。
期待するキーワードとの不一致の可能性があるが、
評価コードによる原因の確認はしていない。
この例は、根拠のない情報を断言した例とは区別して考える必要がある。

## 考察
今回の実験では、5エポックでもJSON形式への準拠率が100％となり、
回答形式は比較的少ない学習でも改善できた。
一方、内容正解率は20エポックの方が高く、
学習時間と正確さの間にトレードオフが見られた。

ただし、形式が整っていても、未知の情報について根拠なく
断言する場合があった。また、全体の正解率が改善しても、
個別の質問では学習後に悪化することが分かった。
形式・内容・未知の質問への対応を分けて評価する必要がある。

ファインチューニングは、決まった回答形式や振る舞いを
学習させる用途に適していると考えた。
一方、最新情報やFAQにない情報の正確さを保証する用途では、
資料の検索や人による確認なども組み合わせる必要がある。

今回は小規模なデータによる各条件1回の比較であり、
別の質問やデータでも同じ傾向になるかは未確認である。