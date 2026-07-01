import { app } from "../../../scripts/app.js";

const MAX_LORAS = 20;

function findWidget(node, name) {
  return node.widgets?.find((widget) => widget.name === name);
}

function hasInput(node, name) {
  return node.inputs?.some((input) => input.name === name) ?? false;
}

function setWidgetVisible(widget, visible) {
  if (!widget) {
    return;
  }

  widget.hidden = !visible;
  if (widget.options) {
    widget.options.hidden = !visible;
  }
}

function resizeNode(node) {
  const size = node.computeSize();
  node.setSize([Math.max(node.size[0], size[0]), size[1]]);
  node.setDirtyCanvas(true, true);
}

function syncLoraNameList(node) {
  const count = Number(findWidget(node, "lora_count")?.value ?? 0);

  for (let i = 1; i <= MAX_LORAS; i++) {
    const widget = findWidget(node, `lora_name_${i}`);
    if (hasInput(node, widget?.name)) {
      continue;
    }
    setWidgetVisible(widget, i <= count);
  }

  resizeNode(node);
}

app.registerExtension({
  name: "geocine.widgethider",
  nodeCreated(node) {
    if (node.comfyClass !== "LoraNameList") {
      return;
    }

    const loraCountWidget = findWidget(node, "lora_count");
    if (!loraCountWidget) {
      return;
    }

    const originalCallback = loraCountWidget.callback;
    loraCountWidget.callback = function () {
      originalCallback?.apply(this, arguments);
      syncLoraNameList(node);
    };

    syncLoraNameList(node);
  },
});
