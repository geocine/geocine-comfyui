app.registerExtension({
    name: "geocine.widgethider",
    nodeCreated(node) {
        for (const w of node.widgets || []) {
            // Apply widget logic first
            widgetLogic(node, w);
            
            // Skip widgets that already have a value property with a getter/setter
            let originalDescriptor = Object.getOwnPropertyDescriptor(w, 'value');
            if (originalDescriptor && (originalDescriptor.get || originalDescriptor.set)) {
                // Property already has custom getter/setter, don't try to redefine it
                continue;
            }
            
            // For widgets without custom getters/setters, add our own
            let widgetValue = w.value;
            
            try {
                Object.defineProperty(w, 'value', {
                    configurable: true, // Make sure it's configurable for future changes
                    get() {
                        return widgetValue;
                    },
                    set(newVal) {
                        widgetValue = newVal;
                        widgetLogic(node, w);
                    }
                });
            } catch (error) {
                console.warn(`Could not redefine property for widget ${w.name}:`, error);
            }
        }
        setTimeout(() => {initialized = true;}, 500);
    }
}); 