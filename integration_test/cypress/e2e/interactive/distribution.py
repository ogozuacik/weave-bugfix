import random
import weave

# Weave package now defaults to eager mode, but lazy mode required for this example notebook for now.
weave.use_lazy_execution()
from weave.ecosystem import wandb

weave.use_fixed_server_port()

items = weave.save(
    [
        {
            "name": "x",
            "loss1": [random.gauss(5, 2) for i in range(500)],
            "loss2": [random.gauss(5, 2) for i in range(500)],
            "str_val": [random.choice(["a", "b", "c"]) for i in range(500)],
        },
        {
            "name": "y",
            "loss1": [random.gauss(9, 4) for i in range(500)],
            "loss2": [random.gauss(-1, 2) for i in range(500)],
            "str_val": [random.choice(["a", "b", "c"]) for i in range(500)],
        },
    ]
)

panel: wandb.Distribution = wandb.Distribution(
    items, value_fn=lambda x: x["loss1"], label_fn=lambda x: x["str_val"], bin_size=1.5  # type: ignore
)

panel = weave.panels.Board(
    {},
    [
        weave.panels.BoardPanel(
            panel, layout=weave.panels.BoardPanelLayout(x=0, y=0, w=24, h=12)
        )
    ],
)

print(weave.show_url(panel))
