/**
 * theme-toggle.js — Dark mode disabled. Light theme only.
 */
(function () {
  // Clear any stored dark preference so it never applies
  localStorage.removeItem('iq_theme');
  document.documentElement.removeAttribute('data-theme');
})();