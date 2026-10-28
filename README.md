# Cinnastyx

A responsive grid theme with dark, light, gray, and system-preference color schemes.
Tested with **Hugo 0.169.0**. CSS is bundled by Hugo; Sass and Node are not required.

## Local preview

From the theme repository:

```sh
hugo server --source exampleSite
```

## Installation

From a Hugo site repository:

```sh
git submodule add https://github.com/glalonde/cinnastyx.git themes/cinnastyx
```

Set `theme = "cinnastyx"` and your production `baseURL` in your Hugo configuration.
The example site contains a complete configuration, including syntax highlighting
and math delimiters. Use `[pagination] pagerSize = 20` to set the page size.

## Options

Under `[params]`:

- `scheme`: `dark` (default), `light`, `gray`, or `preference` (follows the OS).
- `description`: fallback description for the homepage and list pages.
- `mainSections`: sections included on the homepage, default `["posts"]`.
- `math`: enable KaTeX everywhere; alternatively set `math: true` on a page.

Define navigation in `menu.main`. Set `copyright` to display a footer.
The `head.html` and `foot.html` partials remain available for site overrides.

## Images

A page-bundle image matching `**featured*` is used on its card and article.
Use `featuredAlt` in front matter if the article image conveys information.
Card images are decorative because the adjacent title identifies the article.

For content images, supply meaningful alt text:

```go-html-template
{{< responsive-image src="flower" alt="Cactus flower" sizes="(min-width: 1200px) 1200px, 92vw" >}}
```

Images have intrinsic dimensions, responsive sources without upscaling, and lazy
loading (except the first card and article hero). The optional fourth positional
argument to `imgproc` supplies alt text.

## Math and embeds

The theme loads KaTeX 0.19.1 once on pages that enable math. Keep the Goldmark
passthrough settings from the example config so TeX delimiters survive Markdown.
Inline shortcode execution is unnecessary. KaTeX loads from jsDelivr at runtime.

Use Hugo's current `vimeo` and `youtube` shortcodes. The removed `twitter_simple`
sample has been replaced by a direct X link, so building does not depend on social
media APIs. The example permits raw HTML because its content is trusted; omit
`markup.goldmark.renderer.unsafe` for sites that do not need it.

## Validation

```sh
python3 tests/test_build.py
```

Set `HUGO=/path/to/hugo` if Hugo is not on PATH. The test builds all four schemes
with warnings treated as failures and checks pagination, metadata, images, and
local links under a subdirectory URL. CI also builds the demo.

## Usage in Codespaces

Use the forwarded URL for port 1313 from the Codespaces Ports panel:

```sh
hugo server --source exampleSite --baseURL "https://YOUR-FORWARDED-PORT-URL/" --appendPort=false
```
