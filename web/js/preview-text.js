import { app } from "../../../scripts/app.js";

const ComfyWidgets = window.comfyAPI.widgets.ComfyWidgets;

app.registerExtension({
  name: "geocine.previewText",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name !== "PreviewText") {
      return;
    }

    function isEnabled(value) {
      if (typeof value === "string") {
        return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
      }
      return Boolean(value);
    }

    function stripMarkdownFence(value) {
      const trimmed = value.trim();
      if (!trimmed.startsWith("```")) {
        return value;
      }

      const lines = trimmed.split(/\r?\n/);
      if (lines.length >= 2 && lines[lines.length - 1].trim() === "```") {
        return lines.slice(1, -1).join("\n");
      }

      return value;
    }

    function formatJson(value) {
      let parsed = JSON.parse(stripMarkdownFence(value).trim());

      if (typeof parsed === "string") {
        const nested = parsed.trim();
        if (nested.startsWith("{") || nested.startsWith("[")) {
          parsed = JSON.parse(nested);
        }
      }

      return JSON.stringify(parsed, null, 2);
    }

    function getFormatJsonValue(node) {
      return node.widgets?.find((w) => w.name === "format_json")?.value;
    }

    function formatForPreview(node, value) {
      if (!isEnabled(getFormatJsonValue(node)) || !value.trim()) {
        return value;
      }

      try {
        return formatJson(value);
      } catch {
        return value;
      }
    }

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onNodeCreated?.apply(this, arguments);

      const previewWidget = ComfyWidgets["STRING"](
        this,
        "preview_text",
        ["STRING", { multiline: true }],
        app
      ).widget;

      previewWidget.label = "Preview";
      previewWidget.options.read_only = true;
      previewWidget.options.serialize = false;
      const element = previewWidget.element;
      if (element) {
        element.readOnly = true;
        element.style.opacity = 0.7;
      }
      previewWidget.serialize = false;
    };

    const onExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExecuted?.apply(this, arguments);

      const text = message.text ?? "";
      const value = formatForPreview(
        this,
        Array.isArray(text) ? text.join("\n\n") : String(text)
      );
      const previewWidget = this.widgets?.find((w) => w.name === "preview_text");

      if (previewWidget) {
        previewWidget.value = value;
      }
    };
  },
});
