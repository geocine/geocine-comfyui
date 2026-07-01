import { app } from "../../../scripts/app.js";

const ComfyWidgets = window.comfyAPI.widgets.ComfyWidgets;

app.registerExtension({
  name: "geocine.showtext",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "ShowTextNode") {
      function populate(text) {
        if (this.widgets) {
          // Remove existing text widgets
          for (let i = 1; i < this.widgets.length; i++) {
            this.widgets[i].onRemove?.();
          }
          this.widgets.length = 1;
        }

        const v = [...text];
        if (!v[0]) {
          v.shift();
        }
        for (const list of v) {
          const w = ComfyWidgets["STRING"](
            this,
            "text2",
            ["STRING", { multiline: true }],
            app
          ).widget;
          w.options.read_only = true;
          w.options.serialize = false;
          w.serialize = false;
          const element = w.element;
          if (element) {
            element.readOnly = true;
            element.style.opacity = 0.6;
          }
          w.value = list;
        }

        // Resize the node if needed
        requestAnimationFrame(() => {
          const sz = this.computeSize();
          if (sz[0] < this.size[0]) {
            sz[0] = this.size[0];
          }
          if (sz[1] < this.size[1]) {
            sz[1] = this.size[1];
          }
          this.setSize(sz);
          this.graph?.setDirtyCanvas(true, false);
        });
      }

      // When the node is executed we will be sent the input text, display this in the widget
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        populate.call(this, message.text);
      };

      // Handle configuration (loading from saved workflow)
      const onConfigure = nodeType.prototype.onConfigure;
      nodeType.prototype.onConfigure = function (data) {
        onConfigure?.apply(this, arguments);
        const widgetValues = data?.widgets_values;
        if (widgetValues?.length) {
          const startIndex = widgetValues.length > 1 ? 1 : 0;
          populate.call(this, widgetValues.slice(startIndex));
        }
      };
    }
  },
});
