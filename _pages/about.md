---
permalink: /
title: "Dehao Huang · Robot Learning"
excerpt: "Robotic manipulation and grasping: reducing human intervention in policy post-training and deployment."
author_profile: true
research_media: true
research_index: true
title_id: about
redirect_from:
  - /about/
  - /about.html
---

<div class="profile-intro" id="about">
  <h1>About me</h1>
  <p class="profile-bio">I am <strong>Dehao Huang (黄德豪)</strong>, a Ph.D. candidate at <strong>Southern University of Science and Technology (SUSTech)</strong> in a joint program with <strong>Zhongguancun Academy (ZGCA)</strong>. I work with the <a href="https://rcvlab.eee.sustech.edu.cn/">Robotics and Computer Vision Lab (RCVLab)</a>, advised by Prof. <a href="https://scholar.google.com/citations?hl=en&user=J7UkpAIAAAAJ">Hong Zhang</a> and Prof. <a href="https://scholar.google.com/citations?user=fGv5irIAAAAJ&hl=en&oi=sra">Yue Wang</a>.</p>
  <p class="research-statement">{{ site.data.profile.research_intro }}</p>
  <div class="profile-links" aria-label="Contact and academic profiles">
    <a href="mailto:huangdehao919@gmail.com">Email</a>
    <a href="{{ site.data.profile.scholar }}">Google Scholar</a>
    <a href="https://github.com/red0orange">GitHub</a>
    <a href="{{ '/media/files/cv.pdf' | relative_url }}" aria-label="CV (PDF)">CV <span class="link-format">PDF</span></a>
  </div>
</div>

<div class="section-heading" id="research">
  <div><h2>Research</h2></div>
  <div class="research-filters" role="group" aria-label="Show research" hidden>
    {% assign featured = site.data.publications | where: 'featured', true %}
    <button type="button" data-research-filter="selected" aria-pressed="true" aria-controls="research-list">Selected ({{ featured.size }})</button>
    <button type="button" data-research-filter="all" aria-pressed="false" aria-controls="research-list">All ({{ site.data.publications.size }})</button>
  </div>
</div>
<p class="research-count visually-hidden" aria-live="polite" aria-atomic="true"></p>
<div id="research-list" class="research-list">
{% for paper in site.data.publications %}{% include research-entry.html paper=paper %}{% endfor %}
</div>

<h2 class="background-heading" id="experience">Education & Experience</h2>
<dl class="background-list">
  <div><dt>2024–2027 <span>(expected)</span></dt><dd><strong>Ph.D., Robotics and Smart Manufacturing</strong><br>SUSTech & Zhongguancun Academy</dd></div>
  <div><dt>2024</dt><dd><strong>Algorithm Intern · SenseTime (Yuan Luobo Robotics)</strong><br>Algorithm development and deployment for mobile manipulation robots.</dd></div>
  <div><dt>2022–2024</dt><dd><strong>M.S., Electronic Science and Technology</strong><br>SUSTech</dd></div>
  <div><dt>2018–2022</dt><dd><strong>B.E., Information Engineering</strong><br>South China Normal University</dd></div>
</dl>

<div class="profile-bottom-grid">
<section class="profile-bottom-section" aria-labelledby="open-source">
<h2 id="open-source">Open Source</h2>
<ul class="compact-contributions">
  <li><a href="https://github.com/RLinf/RLinf"><strong>RLinf</strong></a> — Contributions to reinforcement-learning infrastructure for training and evaluating VLA models.</li>
  <li><a href="https://github.com/liyiteng/AlohaMini"><strong>AlohaMini</strong></a> — Contributions to a low-cost mobile manipulation platform for robotics research and education.</li>
</ul>

</section>
<section class="profile-bottom-section" aria-labelledby="awards">
<h2 id="awards">Selected Awards</h2>
<ul class="compact-awards">
  <li><span>2026</span> 1st Academic Research Star, Zhongguancun Academy</li>
  <li><span>2021</span> ICM / MCM Meritorious Winner</li>
  <li><span>2020</span> RoboMaster National Second Prize · National Undergraduate Smart Car Competition Third Prize</li>
</ul>

</section>
</div>
