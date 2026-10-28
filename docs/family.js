'use strict';
// Preserve the previous public player anchors when the root becomes the index.
if (['#experience', '#platforms', '#foundation', '#get-kurtz'].includes(location.hash) && /\/(?:index\.html)?$/.test(location.pathname)) {
  location.replace(new URL(`player/${location.hash}`, location.href));
}
