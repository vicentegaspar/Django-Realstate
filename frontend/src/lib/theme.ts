/**
 * Theme is fixed to dark mode. Kept for potential future use.
 */
export type Theme = 'dark';

export function setTheme(_theme: Theme) {
  if (typeof document === 'undefined') return;
  document.documentElement.classList.remove('light');
  document.documentElement.classList.add('dark');
}
