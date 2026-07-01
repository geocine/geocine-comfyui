import { app } from "../../../../scripts/app.js";

app.registerExtension({
  name: "geocine.loraLoader",
  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== "LoraLoaderStack") {
      return;
    }

    const parseSavedLoras = (values) => {
      const pairs = [];
      if (!Array.isArray(values)) {
        return pairs;
      }

      for (let i = 0; i < values.length; i++) {
        const name = values[i];
        const strength = values[i + 1];
        if (name === "Add LoRA" || name === "Remove LoRA") {
          continue;
        }
        if (typeof name === "string" && typeof strength === "number") {
          pairs.push({ name, strength });
          i++;
        }
      }

      return pairs;
    };

    const getLoraOptions = (node) => {
      for (const widget of node.widgets || []) {
        if (widget?.name?.startsWith("lora_name_")) {
          return widget.options?.values || [];
        }
      }
      return [];
    };

    const getStrengthConfig = (node) => {
      for (const widget of node.widgets || []) {
        if (widget?.name === "lora_strength_1") {
          const options = Object.assign({}, widget.options);
          options.precision = 2;
          return {
            options,
            callback: widget.callback || (() => {}),
          };
        }
      }

      return {
        options: { min: -100.0, max: 100.0, step: 0.01, precision: 2 },
        callback: () => {},
      };
    };

    const countLoraRows = (node) => {
      let maxIndex = 0;
      for (const widget of node.widgets || []) {
        const match = widget?.name?.match(/^lora_name_(\d+)$/);
        if (match) {
          maxIndex = Math.max(maxIndex, Number.parseInt(match[1], 10));
        }
      }
      return maxIndex;
    };

    const addLoraRow = (node, index, name = null, strength = 1.0) => {
      const loraOptions = getLoraOptions(node);
      const strengthConfig = getStrengthConfig(node);
      const combo = node.addWidget(
        "combo",
        `lora_name_${index}`,
        name ?? loraOptions[0] ?? "None",
        () => {},
        { values: loraOptions }
      );
      const number = node.addWidget(
        "number",
        `lora_strength_${index}`,
        strength,
        strengthConfig.callback,
        strengthConfig.options
      );
      return { combo, number };
    };

    const ensureLoraRows = (node, count) => {
      for (let i = countLoraRows(node) + 1; i <= count; i++) {
        addLoraRow(node, i);
      }
    };

    const applySavedLoras = (node, pairs) => {
      pairs.forEach((pair, i) => {
        const index = i + 1;
        const nameWidget = node.widgets?.find((w) => w?.name === `lora_name_${index}`);
        const strengthWidget = node.widgets?.find((w) => w?.name === `lora_strength_${index}`);
        if (nameWidget) {
          nameWidget.value = pair.name;
        }
        if (strengthWidget) {
          strengthWidget.value = pair.strength;
        }
      });
    };

    const resizeNode = (node, keepWidth = true) => {
      const size = node.computeSize();
      node.setSize([keepWidth ? Math.max(node.size[0], size[0]) : size[0], size[1]]);
      node.setDirtyCanvas(true, true);
    };

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const result = onNodeCreated?.apply(this, arguments);

      this.updateRemoveBtn = () => {
        const maxIndex = countLoraRows(this);
        if (maxIndex > 1) {
          if (!this.removeBtn) {
            this.removeBtn = this.addWidget("button", "Remove LoRA", "Remove LoRA", () => {
              const rowIndex = countLoraRows(this);
              if (rowIndex <= 1) {
                return;
              }

              const widgetsToRemove = this.widgets.filter((widget) => {
                return widget?.name === `lora_name_${rowIndex}` || widget?.name === `lora_strength_${rowIndex}`;
              });

              for (const widget of widgetsToRemove) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
              }

              this.updateRemoveBtn();
              resizeNode(this);
            });
            this.removeBtn.serialize = false;
            this.removeBtn.options.serialize = false;
          } else {
            const index = this.widgets.indexOf(this.removeBtn);
            if (index !== -1) {
              this.widgets.splice(index, 1);
              this.widgets.push(this.removeBtn);
            }
          }
        } else if (this.removeBtn) {
          const index = this.widgets.indexOf(this.removeBtn);
          if (index !== -1) {
            this.widgets.splice(index, 1);
          }
          this.removeBtn = null;
        }
      };

      const addBtn = this.addWidget("button", "Add LoRA", "Add LoRA", () => {
        addLoraRow(this, countLoraRows(this) + 1);
        this.updateRemoveBtn();
        resizeNode(this);
      });
      addBtn.serialize = false;
      addBtn.options.serialize = false;
      this.addBtn = addBtn;

      this.widgets.splice(this.widgets.indexOf(addBtn), 1);
      this.widgets.unshift(addBtn);

      const firstStrength = this.widgets.find((widget) => widget?.name === "lora_strength_1");
      if (firstStrength) {
        firstStrength.options.precision = 2;
      }

      this.updateRemoveBtn();

      return result;
    };

    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function (info) {
      const savedLoras = parseSavedLoras(info?.widgets_values);
      ensureLoraRows(this, savedLoras.length);

      const result = onConfigure?.apply(this, arguments);
      applySavedLoras(this, savedLoras);

      if (this.addBtn) {
        this.addBtn.value = "Add LoRA";
      }
      if (this.removeBtn) {
        this.removeBtn.value = "Remove LoRA";
      }

      this.updateRemoveBtn?.();
      resizeNode(this);

      return result;
    };
  },
});
