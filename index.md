---
layout: home
title: Home
---

# Welcome to Alex's Boulder Diary 🏔️

This is a personal diary documenting my experiences and adventures during my 1-year research stay in Boulder, Colorado. Here you'll find daily entries about my academic work and discoveries, physical activities and sports in the Rockies, explorations, cultural experiences, and daily adventures.

## Statistics

Want to see some data about my Boulder adventure? Check out the [statistics page](/alex-goes-usa-diary/stats/) for activity tracking and visualizations.

## Recent Entries

{% assign recent_entries = site.diary | reverse %}
{% for post in recent_entries limit:5 %}
  <div class="diary-entry">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p class="post-meta">{{ post.date | date: "%B %d, %Y" }}</p>
    {% if post.weather %}
      <p><strong>Weather:</strong> {{ post.weather }}</p>
    {% endif %}
    <p>{{ post.excerpt | strip_html | truncate: 200 }}</p>
  </div>
{% endfor %}

## Browse by Tags

<div class="tag-cloud">
{% assign tags = site.diary | map: 'tags' | join: ',' | split: ',' | uniq | sort %}
{% for tag in tags %}
  {% if tag != '' %}
    <a href="{{ '/tags/' | append: tag | downcase | relative_url }}" class="tag">{{ tag }}</a>
  {% endif %}
{% endfor %}
</div>

---

*This diary is powered by Jekyll and hosted on GitHub Pages*
