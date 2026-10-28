---
title: "Image Test"
date: 2021-05-30T14:41:22-07:00
summary: "How to get your free server to do the legwork of image manipulation."
---

So, how do we get responsive images?

At first, I reached for shortcodes, and got about 90% of the way there. But then I realized that shortcodes cannot be invoked from the definition of a shortcode -- only from the body of a piece of content.

So at that point, I reached for partials instead. Partials are slightly less ergonomic because they seem to have some strangeness around argument passing. Arguments can only be passed through a dictionary manually.

This works.

{{<responsive-image  src="cactus_flower" alt="Cactus flower" sizes="(min-width: 1400px) 1400px, 92vw">}}
