/*
Copyright (c) 2024 Streetlives, Inc.

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.
*/

importScripts(
	'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
  );


workbox.routing.registerRoute(
	({request}) => request.destination === 'image',
	new workbox.strategies.NetworkFirst()
)
