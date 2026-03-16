<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchProperties, getImageUrl, type PropertyListItem } from '$lib/api';

  let properties = $state<PropertyListItem[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  onMount(async () => {
    try {
      const res = await fetchProperties({ page: 1 });
      properties = res.items.slice(0, 6);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load properties';
    } finally {
      loading = false;
    }
  });
</script>

<section class="hero">
  <div class="hero-accent"></div>
  <div class="hero-content">
    <h1>Find Your Perfect Property</h1>
    <p class="hero-sub">Browse homes for sale and rent. Modern listings, trusted results.</p>
    <a href="/properties" class="cta">View All Properties</a>
  </div>
</section>

<section class="featured">
  <h2>Featured Listings</h2>
  {#if loading}
    <div class="loading" aria-busy="true">
      <div class="spinner"></div>
      <span>Loading properties...</span>
    </div>
  {:else if error}
    <p class="error">{error}</p>
  {:else if properties.length === 0}
    <p class="empty">No properties yet. Check back soon.</p>
  {:else}
    <div class="grid">
      {#each properties as prop, i (prop.id)}
        <a
          href="/properties/{prop.id}"
          class="card"
          class:featured={i === 0}
          style="animation-delay: {i * 80}ms"
        >
          <div class="card-image">
            {#if prop.thumbnail_url}
              <img src={getImageUrl(prop.thumbnail_url)} alt={prop.title} />
            {:else}
              <div class="placeholder">No image</div>
            {/if}
            <span class="badge">{prop.listing_type === 'sale' ? 'For Sale' : 'For Rent'}</span>
          </div>
          <div class="card-body">
            <h3>{prop.title}</h3>
            <p class="price">{prop.price} {prop.listing_type === 'rent' ? '/ mo' : ''}</p>
            <p class="meta">{prop.city}{prop.region ? `, ${prop.region}` : ''}</p>
            <p class="specs">{prop.bedrooms} bed · {prop.bathrooms} bath{prop.area_sqm ? ` · ${prop.area_sqm} m²` : ''}</p>
          </div>
        </a>
      {/each}
    </div>
    <a href="/properties" class="view-all">View All Properties</a>
  {/if}
</section>

<style>
  .hero {
    position: relative;
    padding: 4rem 0 5rem;
    margin-bottom: 3rem;
    overflow: hidden;
    background: radial-gradient(ellipse 80% 50% at 80% 20%, var(--accent-glow) 0%, transparent 50%);
  }

  .hero-accent {
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 120px;
    background: linear-gradient(180deg, var(--accent) 0%, transparent 100%);
    transform: skewY(-8deg);
    transform-origin: top left;
  }

  .hero-content {
    max-width: 560px;
    text-align: left;
  }

  .hero h1 {
    font-size: clamp(2.5rem, 5vw, 4rem);
    margin: 0 0 1rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }

  .hero-sub {
    font-size: 1.2rem;
    color: var(--fg-muted);
    margin: 0 0 2rem;
    line-height: 1.6;
  }

  .cta {
    display: inline-block;
    padding: 0.875rem 1.75rem;
    background: var(--accent);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    transition: background 0.2s, box-shadow 0.2s;
    box-shadow: 0 0 0 0 var(--accent-glow);
  }

  .cta:hover {
    background: var(--accent-hover);
    color: white;
    box-shadow: 0 0 24px var(--accent-glow);
  }

  .featured {
    animation: fadeUp 0.6s ease-out;
  }

  .featured h2 {
    font-size: 1.75rem;
    margin: 0 0 1.5rem;
    letter-spacing: -0.02em;
  }

  .loading, .error, .empty {
    text-align: center;
    color: var(--fg-muted);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  @keyframes fadeUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .error {
    color: var(--error);
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .card {
    display: block;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    border-left: 3px solid transparent;
    animation: fadeUp 0.5s ease-out backwards;
  }

  .card.featured {
    grid-column: span 2;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--border-strong);
    border-left-color: var(--accent);
  }

  .card.featured .card-image {
    aspect-ratio: 21/10;
  }

  .card-image {
    position: relative;
    aspect-ratio: 16/10;
    background: var(--border);
    overflow: hidden;
  }

  .card-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--fg-muted);
    font-size: 0.9rem;
  }

  .badge {
    position: absolute;
    top: 0.75rem;
    left: 0.75rem;
    padding: 0.25rem 0.5rem;
    background: var(--accent);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    border-radius: 4px;
  }

  .card-body {
    padding: 1.25rem;
  }

  .card-body h3 {
    font-size: 1.25rem;
    margin: 0 0 0.5rem;
    font-weight: 600;
  }

  .price {
    font-weight: 600;
    color: var(--accent);
    margin: 0 0 0.25rem;
  }

  .meta, .specs {
    font-size: 0.9rem;
    color: var(--fg-muted);
    margin: 0;
  }

  .view-all {
    display: block;
    text-align: center;
    margin-top: 2rem;
    font-weight: 600;
  }

  @media (max-width: 900px) {
    .grid {
      grid-template-columns: 1fr;
    }

    .card.featured {
      grid-column: span 1;
    }

    .card.featured .card-image {
      aspect-ratio: 16/10;
    }
  }
</style>
