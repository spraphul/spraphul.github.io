(() => {
 'use strict';
 const root = document.documentElement, toggle = document.querySelector('.theme-toggle');
 let stored;
 try { stored = localStorage.getItem('portfolio-theme'); } catch (_) {}
 const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
 function applyTheme(theme) {
  root.dataset.theme = theme;
  toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
 }
 applyTheme(['dark', 'light'].includes(stored) ? stored : (systemDark.matches ? 'dark' : 'light'));
 toggle.addEventListener('click', () => {
  const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(theme);
  try { localStorage.setItem('portfolio-theme', theme); } catch (_) {}
 });
 const filters = document.querySelector('.filters');
 const buttons = [...filters.querySelectorAll('button')];
 const papers = [...document.querySelectorAll('.paper')];
 filters.hidden = false;
 buttons.forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  papers.forEach(paper => paper.hidden = filter !== 'all' && !paper.dataset.topics.split(' ').includes(filter));
  document.querySelectorAll('.year-group').forEach(group => group.hidden = [...group.querySelectorAll('.paper')].every(paper => paper.hidden));
  const count = papers.filter(paper => !paper.hidden).length;
  document.querySelector('.filter-status').textContent = `${count} publication${count === 1 ? '' : 's'} shown.`;
 }));
 document.getElementById('copyright-year').textContent = new Date().getFullYear();
 const dialog = document.getElementById('figure-dialog');
 const figure = dialog.querySelector('img');
 document.querySelectorAll('.figure-trigger').forEach(trigger => trigger.addEventListener('click', () => {
  figure.src = trigger.dataset.figure;
  figure.alt = trigger.dataset.alt;
  document.getElementById('figure-title').textContent = trigger.dataset.title;
  dialog.querySelector('.figure-paper-link').href = trigger.dataset.paper;
  dialog.showModal();
 }));
 dialog.querySelector('.figure-close').addEventListener('click', () => dialog.close());
 dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
})();
