//#region lib/types/index.js
/**
* Aqua theme-layer plugin, node half.
*
* Upstream this half is an empty `apply()`: the enable flag is a browser-local
* preference and a client-only visual layer owns no host configuration.
*
* Repair history — DSH 0.1.2-rc.1 (patched fork):
* The settings page used to dispatch plugin cards by *served settings
* namespace*, so this half registered an empty pass-through namespace named
* "aqua" whose only job was to make the card dispatchable.
*
* Desktop repair — DSH 0.1.7-rc.2:
* `settings.register` no longer exists on the settings service. 0.1.7 projects
* settings forms from each plugin's own Loader Config instead, so a plugin can
* no longer advertise a namespace, and the 0.1.2-era call only produced
*   [ui-aqua] settings namespace skipped: TypeError: scope.settings.register is not a function
* at every boot. The client half needs no host namespace either: its knobs live
* in the Appearance row (`settings.general.item`, still present in 0.1.7) and
* read/write localStorage on their own. This half is therefore a no-op again.
*/
/**
* Host plugin body: mounts the client half, owns no host state.
* @param _ctx - cordis host context (unused).
*/
function apply(_ctx) {}
//#endregion
export { apply };
