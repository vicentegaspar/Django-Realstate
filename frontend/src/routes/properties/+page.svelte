<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchProperties, fetchFilters, getImageUrl, type PropertyListItem, type FiltersResponse, type PropertyFilters } from '$lib/api';

  let properties = $state<PropertyListItem[]>([]);
  let totalCount = $state(0);
  let filters = $state<FiltersResponse | null>(null);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let filtersOpen = $state(false);

  const PAGE_SIZE = 12;
  let page = $state(1);
  let searchInput = $state('');
  let applied: PropertyFilters = $state({});
  let localFilters: PropertyFilters = $state({});

  async function loadProperties(f: PropertyFilters, p: number) {
    const res = await fetchProperties({ ...f, page: p });
    properties = res.items;
    totalCount = res.count;
  }

  onMount(async () => {
    try {
      const [propsRes, filtersRes] = await Promise.all([
        fetchProperties({ ...applied, page: 1 }),
        fetchFilters()
      ]);
      properties = propsRes.items;
      totalCount = propsRes.count;
      filters = filtersRes;
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load';
    } finally {
      loading = false;
    }
  });

  function toApiFilters(f: PropertyFilters): PropertyFilters {
    const out: PropertyFilters = {};
    if (f.search?.trim()) out.search = f.search.trim();
    if (f.listing_type) out.listing_type = f.listing_type;
    if (f.property_type) out.property_type = f.property_type;
    if (f.city) out.city = f.city;
    if (f.region) out.region = f.region;
    if (f.condition) out.condition = f.condition;
    if (f.sort) out.sort = f.sort;
    if (f.pet_friendly === true) out.pet_friendly = true;
    if (f.furnished === true) out.furnished = true;
    if (f.listed_since) out.listed_since = f.listed_since;
    const n = (v: unknown) => (v === '' || v === undefined ? undefined : Number(v));
    if (n(f.min_price) != null) out.min_price = n(f.min_price);
    if (n(f.max_price) != null) out.max_price = n(f.max_price);
    if (n(f.bedrooms) != null) out.bedrooms = n(f.bedrooms);
    if (n(f.bathrooms) != null) out.bathrooms = n(f.bathrooms);
    if (n(f.min_area) != null) out.min_area = n(f.min_area);
    if (n(f.max_area) != null) out.max_area = n(f.max_area);
    if (n(f.min_lot) != null) out.min_lot = n(f.min_lot);
    if (n(f.max_lot) != null) out.max_lot = n(f.max_lot);
    if (n(f.min_year) != null) out.min_year = n(f.min_year);
    if (n(f.max_year) != null) out.max_year = n(f.max_year);
    if (n(f.parking) != null) out.parking = n(f.parking);
    if (f.features?.length) out.features = f.features;
    return out;
  }

  async function applyFilters() {
    applied = { ...toApiFilters(localFilters), search: searchInput.trim() || undefined };
    page = 1;
    loading = true;
    error = null;
    try {
      await loadProperties(applied, 1);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load';
    } finally {
      loading = false;
    }
    filtersOpen = false;
  }

  function clearFilters() {
    searchInput = '';
    localFilters = {};
    applied = {};
    page = 1;
    loading = true;
    error = null;
    fetchProperties({ page: 1 }).then((res) => {
      properties = res.items;
      totalCount = res.count;
    }).catch((e) => {
      error = e instanceof Error ? e.message : 'Failed to load';
    }).finally(() => {
      loading = false;
    });
    filtersOpen = false;
  }

  async function goToPage(p: number) {
    if (p < 1 || p > totalPages) return;
    page = p;
    loading = true;
    error = null;
    try {
      await loadProperties(applied, p);
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load';
    } finally {
      loading = false;
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const totalPages = $derived(Math.ceil(totalCount / PAGE_SIZE) || 1);
  const startItem = $derived((page - 1) * PAGE_SIZE + 1);
  const endItem = $derived(Math.min(page * PAGE_SIZE, totalCount));

  function toggleFeature(slug: string) {
    const current = (localFilters.features ?? []);
    const next = current.includes(slug)
      ? current.filter((f) => f !== slug)
      : [...current, slug];
    localFilters = { ...localFilters, features: next.length ? next : undefined };
  }
</script>

<div class="page">
  <div class="toolbar">
    <h1>Properties</h1>
    <div class="toolbar-actions">
      <form class="search-form" onsubmit={(e) => { e.preventDefault(); localFilters = { ...localFilters, search: searchInput }; applyFilters(); }}>
        <input
          type="search"
          placeholder="Search by title, address, city..."
          bind:value={searchInput}
          aria-label="Search properties"
          class="search-input"
        />
        <button type="submit" class="btn-search">Search</button>
      </form>
      <button class="filter-btn" onclick={() => (filtersOpen = !filtersOpen)} aria-expanded={filtersOpen}>
        Filters
      </button>
    </div>
  </div>

  <div class="content">
    <aside class="sidebar" class:open={filtersOpen}>
      <div class="sidebar-header">
        <h2>Filters</h2>
        <button class="close-btn" onclick={() => (filtersOpen = false)} aria-label="Close filters">×</button>
      </div>

      {#if filters}
        <form class="filter-form" onsubmit={(e) => { e.preventDefault(); applyFilters(); }}>
          <div class="field">
            <label for="filter-listing">Listing Type</label>
            <select id="filter-listing" bind:value={localFilters.listing_type}>
              <option value="">All</option>
              <option value="sale">For Sale</option>
              <option value="rent">For Rent</option>
            </select>
          </div>

          <div class="field">
            <label for="filter-type">Property Type</label>
            <select id="filter-type" bind:value={localFilters.property_type}>
              <option value="">All</option>
              {#each filters.property_types as pt}
                <option value={pt.slug}>{pt.name}</option>
              {/each}
            </select>
          </div>

          <div class="field-row">
            <div class="field">
              <label for="filter-min-price">Min Price</label>
              <input id="filter-min-price" type="number" bind:value={localFilters.min_price} placeholder="Min" min="0" step="1000" />
            </div>
            <div class="field">
              <label for="filter-max-price">Max Price</label>
              <input id="filter-max-price" type="number" bind:value={localFilters.max_price} placeholder="Max" min="0" step="1000" />
            </div>
          </div>

          <div class="field">
            <label for="filter-bedrooms">Bedrooms</label>
            <select id="filter-bedrooms" bind:value={localFilters.bedrooms}>
              <option value="">Any</option>
              <option value={1}>1+</option>
              <option value={2}>2+</option>
              <option value={3}>3+</option>
              <option value={4}>4+</option>
              <option value={5}>5+</option>
            </select>
          </div>

          <div class="field">
            <label for="filter-bathrooms">Bathrooms</label>
            <select id="filter-bathrooms" bind:value={localFilters.bathrooms}>
              <option value="">Any</option>
              <option value={1}>1+</option>
              <option value={2}>2+</option>
              <option value={3}>3+</option>
              <option value={4}>4+</option>
            </select>
          </div>

          <div class="field-row">
            <div class="field">
              <label for="filter-min-area">Min Area (m²)</label>
              <input id="filter-min-area" type="number" bind:value={localFilters.min_area} placeholder="Min" min="0" step="10" />
            </div>
            <div class="field">
              <label for="filter-max-area">Max Area (m²)</label>
              <input id="filter-max-area" type="number" bind:value={localFilters.max_area} placeholder="Max" min="0" step="10" />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label for="filter-min-lot">Min Lot (m²)</label>
              <input id="filter-min-lot" type="number" bind:value={localFilters.min_lot} placeholder="Min" min="0" step="50" />
            </div>
            <div class="field">
              <label for="filter-max-lot">Max Lot (m²)</label>
              <input id="filter-max-lot" type="number" bind:value={localFilters.max_lot} placeholder="Max" min="0" step="50" />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label for="filter-min-year">Year Built From</label>
              <input id="filter-min-year" type="number" bind:value={localFilters.min_year} placeholder="e.g. 1990" min="1800" max={new Date().getFullYear()} />
            </div>
            <div class="field">
              <label for="filter-max-year">Year Built To</label>
              <input id="filter-max-year" type="number" bind:value={localFilters.max_year} placeholder="e.g. 2020" min="1800" max={new Date().getFullYear()} />
            </div>
          </div>

          <div class="field">
            <label for="filter-parking">Parking Spaces</label>
            <select id="filter-parking" bind:value={localFilters.parking}>
              <option value="">Any</option>
              <option value={1}>1+</option>
              <option value={2}>2+</option>
              <option value={3}>3+</option>
              <option value={4}>4+</option>
            </select>
          </div>

          <div class="field">
            <label for="filter-condition">Condition</label>
            <select id="filter-condition" bind:value={localFilters.condition}>
              <option value="">Any</option>
              {#each filters.conditions || [] as c}
                <option value={c.value}>{c.label}</option>
              {/each}
            </select>
          </div>

          <div class="field">
            <label for="filter-listed">Listed Within</label>
            <select id="filter-listed" bind:value={localFilters.listed_since}>
              <option value="">Any time</option>
              <option value={7}>Last 7 days</option>
              <option value={30}>Last 30 days</option>
              <option value={90}>Last 90 days</option>
            </select>
          </div>

          <div class="field">
            <span class="field-label">Amenities</span>
            <div class="checkboxes" role="group" aria-label="Property amenities">
              <label class="checkbox">
                <input type="checkbox" bind:checked={localFilters.pet_friendly} />
                Pet friendly
              </label>
              <label class="checkbox">
                <input type="checkbox" bind:checked={localFilters.furnished} />
                Furnished
              </label>
            </div>
          </div>

          <div class="field">
            <label for="filter-city">City</label>
            <select id="filter-city" bind:value={localFilters.city}>
              <option value="">All</option>
              {#each filters.cities as city}
                <option value={city}>{city}</option>
              {/each}
            </select>
          </div>

          <div class="field">
            <label for="filter-region">Region</label>
            <select id="filter-region" bind:value={localFilters.region}>
              <option value="">All</option>
              {#each filters.regions || [] as region}
                <option value={region}>{region}</option>
              {/each}
            </select>
          </div>

          <div class="field">
            <span class="field-label">Features</span>
            <div class="checkboxes" role="group" aria-label="Property features">
              {#each filters.features as f}
                <label class="checkbox">
                  <input
                    type="checkbox"
                    checked={(localFilters.features ?? []).includes(f.slug)}
                    onchange={() => toggleFeature(f.slug)}
                  />
                  {f.name}
                </label>
              {/each}
            </div>
          </div>

          <div class="field">
            <label for="filter-sort">Sort</label>
            <select id="filter-sort" bind:value={localFilters.sort}>
              <option value="">Newest</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
            </select>
          </div>

          <div class="actions">
            <button type="button" class="btn-secondary" onclick={clearFilters}>Clear</button>
            <button type="submit" class="btn-primary">Apply</button>
          </div>
        </form>
      {/if}
    </aside>

    <div class="results">
      {#if loading}
        <div class="loading" aria-busy="true">
          <div class="spinner"></div>
          <span>Loading properties...</span>
        </div>
      {:else if error}
        <p class="error">{error}</p>
      {:else if properties.length === 0}
        <div class="empty">
          <p>No properties match your filters.</p>
          <button class="btn-secondary" onclick={clearFilters}>Clear filters</button>
        </div>
      {:else}
        <p class="count">{totalCount} {totalCount === 1 ? 'property' : 'properties'} found</p>
        <div class="grid">
          {#each properties as prop, i (prop.id)}
            <a href="/properties/{prop.id}" class="card" style="animation-delay: {i * 50}ms">
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
        {#if totalCount > PAGE_SIZE}
          <nav class="pagination" aria-label="Property pagination">
            <p class="pagination-info">
              Showing {startItem}–{endItem} of {totalCount}
            </p>
            <div class="pagination-btns">
              <button
                type="button"
                class="btn-secondary"
                disabled={page <= 1}
                onclick={() => goToPage(page - 1)}
              >
                Previous
              </button>
              <span class="page-num">Page {page} of {totalPages}</span>
              <button
                type="button"
                class="btn-secondary"
                disabled={page >= totalPages}
                onclick={() => goToPage(page + 1)}
              >
                Next
              </button>
            </div>
          </nav>
        {/if}
      {/if}
    </div>
  </div>
</div>

<style>
  .page {
    width: 100%;
  }

  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }

  .toolbar h1 {
    margin: 0;
    font-size: 1.75rem;
    letter-spacing: -0.02em;
  }

  .toolbar-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .search-form {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .search-input {
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg-elevated);
    color: var(--fg);
    min-width: 220px;
    font-size: 0.95rem;
  }

  .search-input::placeholder {
    color: var(--fg-muted);
  }

  .search-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }

  .btn-search {
    padding: 0.5rem 1rem;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    transition: background 0.2s, box-shadow 0.2s;
  }

  .btn-search:hover {
    background: var(--accent-hover);
    box-shadow: 0 0 16px var(--accent-glow);
  }

  .filter-btn {
    display: none;
    padding: 0.5rem 1rem;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--fg);
    font-weight: 500;
  }

  .filter-btn:hover {
    border-color: var(--accent);
    background: var(--bg-subtle);
  }

  .content {
    display: flex;
    gap: 2rem;
    align-items: flex-start;
  }

  .sidebar {
    width: 280px;
    flex-shrink: 0;
    max-height: calc(100vh - 140px);
    overflow-y: auto;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    position: sticky;
    top: 100px;
  }

  .field input:focus,
  .field select:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-glow);
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .sidebar-header h2 {
    margin: 0;
    font-size: 1.25rem;
  }

  .close-btn {
    display: none;
    background: none;
    border: none;
    font-size: 1.5rem;
    color: var(--fg-muted);
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }

  .filter-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .field label,
  .field .field-label {
    display: block;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.35rem;
    color: var(--fg-muted);
  }

  .field input,
  .field select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--bg);
    color: var(--fg);
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .field-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .checkboxes {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    cursor: pointer;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
  }

  .btn-primary {
    flex: 1;
    padding: 0.6rem 1rem;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: background 0.2s, box-shadow 0.2s;
  }

  .btn-primary:hover {
    background: var(--accent-hover);
    box-shadow: 0 0 16px var(--accent-glow);
  }

  .btn-secondary {
    padding: 0.6rem 1rem;
    background: transparent;
    color: var(--fg);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-weight: 500;
    transition: border-color 0.2s, background 0.2s;
  }

  .btn-secondary:hover:not(:disabled) {
    border-color: var(--border-strong);
    background: var(--bg-subtle);
  }

  .results {
    flex: 1;
    min-width: 0;
  }

  .count {
    font-size: 0.9rem;
    color: var(--fg-muted);
    margin: 0 0 1rem;
  }

  .pagination {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .pagination-info {
    font-size: 0.9rem;
    color: var(--fg-muted);
    margin: 0;
  }

  .pagination-btns {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .pagination-btns .btn-secondary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .page-num {
    font-size: 0.9rem;
    color: var(--fg-muted);
  }

  .loading, .error, .empty {
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

  .error {
    color: var(--error);
  }

  .empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .card {
    display: block;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-left: 3px solid transparent;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    animation: fadeUp 0.5s ease-out backwards;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--border-strong);
    border-left-color: var(--accent);
  }

  @keyframes fadeUp {
    from {
      opacity: 0;
      transform: translateY(16px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
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
    font-size: 1.15rem;
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

  @media (max-width: 768px) {
    .toolbar {
      flex-direction: column;
      align-items: stretch;
    }

    .search-form {
      flex: 1;
    }

    .search-input {
      min-width: 0;
    }

    .filter-btn {
      display: block;
    }

    .sidebar {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      width: 100%;
      max-height: 100vh;
      overflow-y: auto;
      z-index: 200;
      border-radius: 0;
    }

    .sidebar.open {
      display: block;
    }

    .close-btn {
      display: block;
    }
  }
</style>
