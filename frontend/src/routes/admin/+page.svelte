<script lang="ts">
  import { getBaseUrl } from '$lib/api';
  const ADMIN_URL = `${getBaseUrl()}/admin/`;
</script>

<section class="admin-section">
  <h1>Admin</h1>
  <p class="intro">
    Manage properties, property types, and features from the Django admin panel.
  </p>
  <a href={ADMIN_URL} target="_blank" rel="noopener noreferrer" class="admin-link">
    Open Django Admin
  </a>
  <p class="hint">
    You will need to log in with a staff account. Create one with:
    <code>python backend/manage.py createsuperuser</code>
  </p>
</section>

<style>
  .admin-section {
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
    padding: 3rem 1.5rem;
  }

  .admin-section h1 {
    margin: 0 0 1rem;
    font-size: 1.75rem;
    letter-spacing: -0.02em;
  }

  .intro {
    color: var(--fg-muted);
    margin: 0 0 1.5rem;
    line-height: 1.6;
  }

  .admin-link {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background: var(--accent);
    color: white;
    border-radius: 8px;
    font-weight: 600;
    transition: background 0.2s, box-shadow 0.2s;
  }

  .admin-link:hover {
    background: var(--accent-hover);
    color: white;
    box-shadow: 0 0 24px var(--accent-glow);
  }

  .hint {
    margin-top: 2rem;
    font-size: 0.9rem;
    color: var(--fg-muted);
  }

  .hint code {
    display: block;
    margin-top: 0.5rem;
    padding: 0.75rem;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.85rem;
    text-align: left;
  }
</style>
