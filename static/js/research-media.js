/* Keep third-party players off the page until a visitor chooses to watch. */
(function () {
  'use strict';
  document.querySelectorAll('.research-entry').forEach(function (entry) {
    entry.addEventListener('research:hidden', function () {
      var player = entry.querySelector('.research-video');
      if (!player || !player.researchPreview) return;
      if (player.tagName === 'VIDEO') player.pause();
      player.replaceWith(player.researchPreview);
      entry.classList.remove('is-playing');
    });
  });
  document.addEventListener('click', function (event) {
    var preview = event.target.closest('.video-preview');
    if (!preview || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    var player;
    if (preview.dataset.videoFile) {
      player = document.createElement('video');
      player.className = 'research-video';
      player.controls = true;
      player.playsInline = true;
      player.src = preview.dataset.videoFile;
      player.poster = preview.querySelector('img').src;
    } else {
      player = document.createElement('iframe');
      player.className = 'research-video';
      player.src = preview.dataset.videoEmbed + '?autoplay=1';
      player.title = preview.getAttribute('aria-label');
      player.allow = 'autoplay; encrypted-media; picture-in-picture';
      player.allowFullscreen = true;
    }
    player.setAttribute('aria-label', preview.getAttribute('aria-label'));
    player.tabIndex = 0;
    player.researchPreview = preview;
    var entry = preview.closest('.research-entry');
    if (entry) entry.classList.add('is-playing');
    preview.replaceWith(player);
    player.focus();
    if (player.tagName === 'VIDEO') player.play().catch(function () { /* Native controls remain available. */ });
  });
}());
