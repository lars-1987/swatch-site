# Swatch

A free, single-file colour palette tool. Browse a curated set of palettes, build
your own with colour theory, check contrast, and export anywhere.

Live at [tryswatch.com](https://tryswatch.com).

## What it is

- One `index.html`, no build step, no framework.
- Works with JavaScript off, honours `prefers-reduced-motion`, targets WCAG AA.
- Everything is self-hosted. Fonts and libraries ship from `vendor/`, so there
  are zero third-party calls.

## Structure

- `index.html` the tool itself, served at `/`
- `privacy/`, `terms/` legal pages
- `vendor/` self-hosted fonts plus GSAP, ScrollTrigger, Lenis and three.js
- `favicon.svg`, `og.png` site icon and social card
- `build-og.py` regenerates `og.png` (needs PIL, fonttools, brotli)

## Licence

Copyright (c) 2026 Lars Holmstrom. All rights reserved.

This source is published for transparency only. No permission is granted to copy,
modify, redistribute, or reuse any part of it. The colour palettes you create and
export with Swatch are yours to use however you like, commercial work included.
