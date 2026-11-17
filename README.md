# Coding Agent Evaluation Work Sample

A runnable example of how I evaluate coding solutions against a task specification. The example uses three demonstration implementations and four synthetic CSV fixtures. It accompanies my broader coding-agent evaluation dashboard, which combines deterministic tests with evidence-linked human review.

## A failure worth inspecting

The task is to remove exact duplicate **rows**, keep the first occurrence, and preserve every field as text. Both rows below belong in the output because their statuses differ.

| ID | Name | Status |
| --- | --- | --- |
| `001` | Ari | `open` |
| `001` | Ari | `closed` |

The first-row-per-ID implementation keeps the `open` row and drops the `closed` row. A basic duplicate-row test passes for this implementation. The shared-ID fixture reveals why that passing test is insufficient.

**Reviewer note.** Mark this as a functional correctness failure. The implementation silently drops a valid status record. Compare complete parsed rows, then rerun the shared-ID fixture and check that genuine duplicates still collapse.

## Run the sample

Use Python 3.10 or newer. The sample uses the standard library.

```sh
python evaluate.py
python -m unittest -v
```

| Implementation | Fixtures passed | What the results show |
| --- | ---: | --- |
| Exact-row deduplication | 4/4 | Preserves distinct rows, leading zeros, whitespace, and empty cells across the sample. |
| First row per ID | 2/4 | Drops distinct rows that share an ID. |
| Filter rows with empty cells | 3/4 | Discards valid rows with a blank field. |

The first command prints expected and actual rows for each failure. The second verifies the documented failure set and checks that the evidence identifies the dropped row.

## Inspect the work

- [Fixture inputs and expected outputs](fixtures.json)
- [Candidate implementations and evaluation runner](evaluate.py)
- [Regression tests](test_evaluate.py)

This sample covers a small, well-formed CSV task and uses deliberately flawed demonstration candidates. The counts describe these fixtures and implementations.
