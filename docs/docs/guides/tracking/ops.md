---
sidebar_position: 1
hide_table_of_contents: true
---

# Ops

A Weave op is a versioned function that automatically logs all calls.

To create an op, decorate a python function with `weave.op()`

```python
@weave.op()
def track_me(v):
    return v + 5

weave.init()
track_me(15)
```

Calling an op will created a new op version if the code has changed from the last call, and log the inputs and outputs of the function.

:::note
Functions decorated with `@weave.op()` will behave normally (without code versioning and tracking), if you don't call `weave.init()` before calling them.
:::

Ops can be [served](/guides/tools/serve) or [deployed](/guides/tools/deploy) using the Weave toolbelt.
