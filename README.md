# family-history-archive

[English](./README.en.md)

運営者の先祖のうち、故人についての一次史料の翻刻が、運営者のリポジトリのどこにあるかを並べる索引です。
索引に置くのは、所在・出典・権利・読んだ日だけです。
翻刻そのものは、ここに写しません。
各項目は、史料がすでにある場所を指します。
この索引は、2026-11-20 に置きました。

保存版は Zenodo にあります。
最初の版の DOI は [`10.5281/zenodo.24397144`](https://doi.org/10.5281/zenodo.24397144) です。
すべての版に共通する DOI は [`10.5281/zenodo.24397143`](https://doi.org/10.5281/zenodo.24397143) です。

## 利益相反

運営者は、この索引が挙げる人物の子孫です。
naval-gazette-notes の README は、大谷恒を著者の外曾祖父と書いています。
同じリポジトリの正誤表の N5 は、この史料を調べた動機が血縁であると書いています。
子孫が先祖の史料を並べると、何を選ぶか、どう読むかが、先祖の側へ寄ることがあります。
この索引は、史料の読みを足しません。
読みと、確定できることとできないことは、それぞれの所在の記録に従います。
史料が述べることと、家に伝わることを、同じ項目に混ぜません。

## 索引

項目は 2 件です。
どの項目も、運営者のリポジトリの main にある所在を指します。

| 番号 | 人物 | 史料 | 翻刻 | 所在 | 権利 | 読んだ日 |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 大谷恒 | JACAR（アジア歴史資料センター）Ref.C12070491000、海軍公報（部内限）號外　昭和十八年九月十一日發令（防衛省防衛研究所） | 史料ノートの第3節の翻刻（凍結した PDF） | [naval-gazette-notes の pdf/naval-gazette-entry-otani-tsune.pdf](https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/pdf/naval-gazette-entry-otani-tsune.pdf)（DOI [10.5281/zenodo.22055709](https://doi.org/10.5281/zenodo.22055709)） | CC BY 4.0。公報そのものの扱いは、naval-gazette-notes が決めていません。原資料の画像は、どこにも置いていません。 | 2026-11-20 |
| F2 | 大谷恒 | JACAR（アジア歴史資料センター）Ref.C12070491000、海軍公報（部内限）號外　昭和十八年九月十一日發令（防衛省防衛研究所） | 同じ翻刻の機械可読の形（CSV と JSON） | [naval-gazette-notes の data/investiture-1943-09-11.csv](https://github.com/cpsbvbng26-dotcom/naval-gazette-notes/blob/main/data/investiture-1943-09-11.csv) | CC BY 4.0。公報そのものの扱いは、naval-gazette-notes が決めていません。原資料の画像は、どこにも置いていません。 | 2026-11-20 |

| 人物 | 続柄 | 故人であることと続柄の出どころ |
| --- | --- | --- |
| 大谷恒 | 外曾祖父 | naval-gazette-notes の README の「扱う人」と「史料の外にあるもの」 |

DOI は、naval-gazette-notes の README に書かれた番号を写したものです。
その README は、2026-11-11 に DataCite の記録で版を確かめたと書いています。
この索引の作業では、DataCite に当たっていません。

## 入れていないもの

- かつて cpsbvbng26-dotcom に、先祖の公的記録の頁がありました。
- その頁は、2026-09-11 に運営者の指示で消されました。self-correction の SC-032 が、そのことを記録しています。
- この索引は、その頁の中身を戻しません。
- その頁が挙げていた大谷恒のほかの人物には、いま公開している一次史料の翻刻がありません。そのため、この索引には入れていません。
- cpsbvbng26-dotcom の外部の評価の記録には、〔氏名を伏せた一名〕がいます。
- 伏せた理由は、存命かどうかを確かめていないことです。self-correction の SC-023 が、そのことを記録しています。
- この索引でも、その名を書きません。伏せた決めは、そのまま保ちます。
- 戸籍と除籍の記載の中身、その画像と転写、本籍は置きません。
- JACAR の原資料の画像は置きません。cpsbvbng26-dotcom の決めごと 11 により、防衛省防衛研究所 戦史研究センターへの連絡が先です。
- naval-gazette-notes の README の「史料の外にあるもの」は、報道・照会・家に伝わること・家にあった物です。一次史料の翻刻ではないので、入れていません。
- 同じ名簿のほかの受章者は、先祖ではないので挙げません。名も写しません。

## 項目の欄

| 欄 | 中身 |
| --- | --- |
| `id` | 番号。F から始まる |
| `person` | 人物。公開している記録が故人だと述べ、続柄を述べている人だけ |
| `primary_source` | 一次史料の出典表記。所在の記録が定めた形のまま |
| `jacar` | JACAR の参照コード |
| `transcription_ja`・`transcription_en` | 翻刻が何か |
| `location` | 翻刻がすでにある場所 |
| `doi` | 所在の記録が書いた DOI。無ければ `null` |
| `rights_ja`・`rights_en` | 権利。所在の記録のライセンスと、原資料の扱い |
| `repository`・`commit` | 所在のリポジトリと、読んだときの main のコミット |
| `read` | 読んだ日 |
| `sources` | `verification/sources.json` の引用の名 |

## 検査

```
python3 verification/check.py            # 索引の欄・出どころの引用・故人と続柄・伏せた名・画像・続柄の語・消した頁・開示・写し・書き方・数
python3 verification/check.py --online   # 所在と出どころを各リポジトリの main から取り寄せ直し、所在があり、引用がいまもあるかを見る
python3 verification/check.py --break    # 検査を一つずつ壊し、落ちることを確かめる
```

伏せた名は、この検査の中でも、名そのものではなく SHA-256 の値でだけ持ちます。
そのため、壊して確かめる検査は、名の代わりに検査用の語を足して、同じ仕組みが落ちることを確かめます。

CI は、外へ出ない検査と壊して確かめる検査を、push と PR のたびに回します。
取り寄せ直す検査は、別の仕事として同じときと週に一度回します。

## 運営者

運営者は、根本卓哉（Takuya Nemoto）です。
ORCID iD は [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547) です。
誤りは[誤りの知らせ](https://github.com/cpsbvbng26-dotcom/family-history-archive/issues/new?template=error-report.yml)の様式で受けます。
安全の問題は、[SECURITY.md](./SECURITY.md) の入口で受けます。
索引が指す史料の人物についての求めは、所在の側の窓口で受けます。
naval-gazette-notes の README は、その窓口として cpsbvbng26-dotcom の[免責事項](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/DISCLAIMER.md)の「人についての記載」を挙げています。

## 言語モデルの使い方

言語モデルの使い方を、ほかのリポジトリと同じ形の表にしています。

| 道具 | 使ったところ | 確かめた人 |
| --- | --- | --- |
| Claude Code（Anthropic） | 索引の項目、README の文、`verification/` の検査、所在の記録からの引用 | `verification/check.py` の検査。運営者が読んで確かめた記録はありません |

索引の項目は、Claude Code が所在の記録を 2026-11-20 に読んで書きました。
史料そのものは読み直していません。
Claude は著者ではありません。

## ライセンス

索引と文は [CC BY 4.0](./LICENSE)、コードは [MIT](./LICENSE-CODE) です。
所在の側の翻刻とデータの権利は、それぞれの所在のライセンスによります。
