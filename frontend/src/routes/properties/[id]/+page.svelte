<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { fetchProperty, getImageUrl, submitInquiry, type PropertyDetail } from '$lib/api';

  let property = $state<PropertyDetail | null>(null);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let activeImage = $state(0);

  let inquiryName = $state('');
  let inquiryEmail = $state('');
  let inquiryPhone = $state('');
  let inquiryMessage = $state('');
  let inquirySubmitting = $state(false);
  let inquirySuccess = $state(false);
  let inquiryError = $state<string | null>(null);

  const id = $derived(Number($page.params.id));

  onMount(async () => {
    try {
      property = await fetchProperty(id);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Property not found';
    } finally {
      loading = false;
    }
  });

  async function handleInquirySubmit(e: Event) {
    e.preventDefault();
    if (!property) return;
    inquiryError = null;
    inquirySubmitting = true;
    try {
      await submitInquiry(property.id, {
        name: inquiryName,
        email: inquiryEmail,
        phone: inquiryPhone || undefined,
        message: inquiryMessage,
      });
      inquirySuccess = true;
      inquiryName = '';
      inquiryEmail = '';
      inquiryPhone = '';
      inquiryMessage = '';
    } catch (err) {
      inquiryError = err instanceof Error ? err.message : 'Failed to send inquiry';
    } finally {
      inquirySubmitting = false;
    }
  }
</script>

{#if loading}
  <div class="loading" aria-busy="true">
    <div class="spinner"></div>
    <span>Loading property...</span>
  </div>
{:else if error}
  <div class="error">
    <p>{error}</p>
    <a href="/properties">Back to listings</a>
  </div>
{:else if property}
  <article class="detail">
    <a href="/properties" class="back">← Back to properties</a>

    <div class="gallery">
      <div class="main-image">
        {#if property.images?.length}
          <img
            src={getImageUrl(property.images[activeImage]?.image)}
            alt={property.title}
          />
        {:else if property.thumbnail_url}
          <img src={getImageUrl(property.thumbnail_url)} alt={property.title} />
        {:else}
          <div class="placeholder">No image</div>
        {/if}
      </div>
      {#if property.images && property.images.length > 1}
        <div class="thumbnails">
          {#each property.images as img, i}
            <button
              type="button"
              class="thumb"
              class:active={i === activeImage}
              onclick={() => (activeImage = i)}
            >
              <img src={getImageUrl(img.image)} alt={img.caption || `Image ${i + 1}`} />
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <div class="content">
      <header>
        <span class="badge">{property.listing_type === 'sale' ? 'For Sale' : 'For Rent'}</span>
        <h1>{property.title}</h1>
        <p class="price">{property.price} {property.listing_type === 'rent' ? '/ month' : ''}</p>
        <p class="location">
          {property.address && `${property.address}, `}
          {property.city}
          {property.region && `, ${property.region}`}
          {property.country && `, ${property.country}`}
        </p>
      </header>

      <div class="specs">
        <div class="spec">
          <span class="label">Bedrooms</span>
          <span class="value">{property.bedrooms}</span>
        </div>
        <div class="spec">
          <span class="label">Bathrooms</span>
          <span class="value">{property.bathrooms}</span>
        </div>
        {#if property.area_sqm}
          <div class="spec">
            <span class="label">Area</span>
            <span class="value">{property.area_sqm} m²</span>
          </div>
        {/if}
        {#if property.lot_sqm}
          <div class="spec">
            <span class="label">Lot Size</span>
            <span class="value">{property.lot_sqm} m²</span>
          </div>
        {/if}
        {#if property.parking_spaces != null && property.parking_spaces > 0}
          <div class="spec">
            <span class="label">Parking</span>
            <span class="value">{property.parking_spaces}</span>
          </div>
        {/if}
        {#if property.year_built}
          <div class="spec">
            <span class="label">Year Built</span>
            <span class="value">{property.year_built}</span>
          </div>
        {/if}
        {#if property.condition}
          <div class="spec">
            <span class="label">Condition</span>
            <span class="value">{
              property.condition === 'new' ? 'New Construction' :
              property.condition === 'renovated' ? 'Renovated' :
              property.condition === 'good' ? 'Good Condition' :
              property.condition === 'needs_work' ? 'Needs Work' : property.condition
            }</span>
          </div>
        {/if}
        {#if property.property_type}
          <div class="spec">
            <span class="label">Type</span>
            <span class="value">{property.property_type}</span>
          </div>
        {/if}
        {#if property.pet_friendly || property.furnished}
          <div class="spec">
            <span class="label">Amenities</span>
            <span class="value">
              {[property.pet_friendly && 'Pet friendly', property.furnished && 'Furnished'].filter(Boolean).join(', ')}
            </span>
          </div>
        {/if}
      </div>

      {#if property.description}
        <section class="description">
          <h2>Description</h2>
          <p>{property.description}</p>
        </section>
      {/if}

      {#if property.features?.length}
        <section class="features">
          <h2>Features</h2>
          <ul>
            {#each property.features as f}
              <li>{f}</li>
            {/each}
          </ul>
        </section>
      {/if}

      <section class="inquiry">
        <h2>Contact About This Property</h2>
        {#if inquirySuccess}
          <p class="inquiry-success">Thank you! Your inquiry has been sent. We'll get back to you soon.</p>
        {:else}
          <form class="inquiry-form" onsubmit={handleInquirySubmit}>
            <div class="form-row">
              <div class="field">
                <label for="inquiry-name">Name *</label>
                <input id="inquiry-name" type="text" bind:value={inquiryName} required placeholder="Your name" />
              </div>
              <div class="field">
                <label for="inquiry-email">Email *</label>
                <input id="inquiry-email" type="email" bind:value={inquiryEmail} required placeholder="your@email.com" />
              </div>
            </div>
            <div class="field">
              <label for="inquiry-phone">Phone</label>
              <input id="inquiry-phone" type="tel" bind:value={inquiryPhone} placeholder="Optional" />
            </div>
            <div class="field">
              <label for="inquiry-message">Message *</label>
              <textarea id="inquiry-message" bind:value={inquiryMessage} required placeholder="Your message or questions about this property..." rows="4"></textarea>
            </div>
            {#if inquiryError}
              <p class="form-error">{inquiryError}</p>
            {/if}
            <button type="submit" class="btn-submit" disabled={inquirySubmitting}>
              {inquirySubmitting ? 'Sending...' : 'Send Inquiry'}
            </button>
          </form>
        {/if}
      </section>
    </div>
  </article>
{/if}

<style>
  .loading, .error {
    text-align: center;
    padding: 3rem;
    color: var(--fg-muted);
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

  .error a {
    display: inline-block;
    margin-top: 1rem;
  }

  .detail {
    max-width: 900px;
    margin: 0 auto;
  }

  .back {
    display: inline-block;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    color: var(--fg-muted);
  }

  .back:hover {
    color: var(--accent);
  }

  .gallery {
    margin-bottom: 2rem;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
    background: var(--bg-elevated);
  }

  .main-image {
    aspect-ratio: 16/10;
    background: var(--border);
    overflow: hidden;
  }

  .main-image img {
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
  }

  .thumbnails {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    overflow-x: auto;
  }

  .thumb {
    flex-shrink: 0;
    width: 80px;
    height: 60px;
    padding: 0;
    border: 2px solid transparent;
    border-radius: 6px;
    overflow: hidden;
    cursor: pointer;
    background: var(--border);
  }

  .thumb {
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .thumb.active {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-glow);
  }

  .thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .content header {
    margin-bottom: 1.5rem;
  }

  .badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background: var(--accent);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    border-radius: 4px;
    margin-bottom: 0.75rem;
  }

  .content h1 {
    font-size: 2rem;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
  }

  .price {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--accent);
    margin: 0 0 0.5rem;
  }

  .location {
    color: var(--fg-muted);
    margin: 0;
  }

  .specs {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    padding: 1.5rem 0;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
  }

  .spec {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .spec .label {
    font-size: 0.85rem;
    color: var(--fg-muted);
  }

  .spec .value {
    font-weight: 600;
  }

  .description, .features {
    margin-bottom: 2rem;
  }

  .description h2, .features h2 {
    font-size: 1.25rem;
    margin: 0 0 0.75rem;
  }

  .description p {
    margin: 0;
    line-height: 1.7;
    color: var(--fg-muted);
  }

  .features ul {
    margin: 0;
    padding-left: 1.25rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 0.5rem;
  }

  .inquiry {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
  }

  .inquiry h2 {
    font-size: 1.25rem;
    margin: 0 0 1rem;
  }

  .inquiry-success {
    color: var(--accent);
    font-weight: 500;
  }

  .inquiry-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 500px;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .inquiry-form .field label {
    display: block;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.35rem;
    color: var(--fg-muted);
  }

  .inquiry-form input,
  .inquiry-form textarea {
    width: 100%;
    padding: 0.6rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg);
    color: var(--fg);
    font-family: inherit;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .inquiry-form textarea {
    resize: vertical;
    min-height: 100px;
  }

  .inquiry-form input:focus,
  .inquiry-form textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }

  .form-error {
    color: var(--error);
    font-size: 0.9rem;
    margin: 0;
  }

  .btn-submit {
    padding: 0.75rem 1.5rem;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    align-self: flex-start;
    transition: background 0.2s, box-shadow 0.2s;
  }

  .btn-submit:hover:not(:disabled) {
    background: var(--accent-hover);
    box-shadow: 0 0 20px var(--accent-glow);
  }

  .btn-submit:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  @media (max-width: 500px) {
    .form-row {
      grid-template-columns: 1fr;
    }
  }
</style>
