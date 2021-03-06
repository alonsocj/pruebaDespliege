/* *
 *
 *  Copyright (c) 2019-2020 Highsoft AS
 *
 *  Boost module: stripped-down renderer for higher performance
 *
 *  License: highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */
'use strict';
import H from '../../parts/Globals.js';
import butils from './boost-utils.js';
import init from './boost-init.js';
import './boost-overrides.js';
import './named-colors.js';
import U from '../../parts/Utilities.js';
var error = U.error;
// These need to be fixed when we support named imports
var hasWebGLSupport = butils.hasWebGLSupport;
if (!hasWebGLSupport()) {
    if (typeof H.initCanvasBoost !== 'undefined') {
        // Fallback to canvas boost
        H.initCanvasBoost();
    }
    else {
        error(26);
    }
}
else {
    // WebGL support is alright, and we're good to go.
    init();
}
