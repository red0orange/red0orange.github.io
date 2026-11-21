/* One research list: selected work by default, all papers without JavaScript. */
(function () {
  'use strict';
  var list = document.getElementById('research-list');
  var controls = document.querySelector('.research-filters');
  if (!list || !controls) return;
  var entries = Array.from(list.querySelectorAll('.research-entry'));
  var buttons = Array.from(controls.querySelectorAll('button'));
  var status = document.querySelector('.research-count');

  function filter(value) {
    var count = 0;
    entries.forEach(function (entry) {
      var hide = value === 'selected' && entry.dataset.featured !== 'true';
      if (hide && !entry.hidden) entry.dispatchEvent(new Event('research:hidden'));
      entry.hidden = hide;
      if (!hide) count += 1;
    });
    buttons.forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.researchFilter === value));
    });
    status.textContent = 'Showing ' + count + ' of ' + entries.length + ' research publications.';
  }

  function revealLinkedPaper() {
    var id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { return; }
    var target = document.getElementById(id);
    if (target && target.classList.contains('research-entry')) {
      if (target.hidden) filter('all');
      target.scrollIntoView();
    }
  }

  buttons.forEach(function (button) {
    button.addEventListener('click', function () { filter(button.dataset.researchFilter); });
  });
  filter('selected');
  controls.hidden = false;
  revealLinkedPaper();
  window.addEventListener('hashchange', revealLinkedPaper);

  var nav = document.getElementById('site-nav');
  var sectionLinks = Array.from(nav.querySelectorAll('a')).filter(function (link) {
    return link.origin === location.origin && link.pathname === location.pathname && link.hash && document.getElementById(link.hash.slice(1));
  });
  function updateNavigation() {
    var current = sectionLinks[0];
    sectionLinks.forEach(function (link) {
      if (document.getElementById(link.hash.slice(1)).getBoundingClientRect().top <= 140) current = link;
    });
    sectionLinks.forEach(function (link) {
      if (link === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  var queued = false;
  window.addEventListener('scroll', function () {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(function () { updateNavigation(); queued = false; });
  }, { passive: true });
  nav.addEventListener('click', function (event) {
    var link = event.target.closest('a');
    if (!link || sectionLinks.indexOf(link) < 0 || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    // Use native section URLs instead of the theme's URL-less smooth scrolling.
    event.preventDefault();
    event.stopPropagation();
    window.location.hash = link.hash;
    document.getElementById(link.hash.slice(1)).scrollIntoView();
    nav.querySelector('.hidden-links').classList.add('hidden');
    nav.querySelector('button').classList.remove('close');
  }, true);
  updateNavigation();
}());
