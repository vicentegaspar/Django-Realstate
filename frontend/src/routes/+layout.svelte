<script lang="ts">
  import '../app.css';

  let { children } = $props();
</script>

<svelte:head>
  <title>Real Estate</title>
</svelte:head>

<header class="header">
  <nav class="nav">
    <a href="/" class="logo">Real Estate</a>
    <div class="nav-links">
      <a href="/properties" class="nav-link">Properties</a>
      <a href="/admin" class="nav-link admin-link">Admin</a>
    </div>
  </nav>
</header>

<main class="main">
  {@render children()}
</main>

<footer class="footer">
  <p>&copy; {new Date().getFullYear()} Real Estate. All rights reserved.</p>
</footer>

<style>
  .header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--bg-elevated);
    border-bottom: 1px solid var(--border);
    box-shadow: var(--shadow);
    backdrop-filter: blur(8px);
  }

  .nav {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--fg);
    letter-spacing: -0.02em;
  }

  .logo:hover {
    color: var(--accent);
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .nav-link {
    position: relative;
    color: var(--fg-muted);
    font-weight: 500;
    padding-bottom: 0.25rem;
  }

  .nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--accent);
    transition: width 0.2s ease;
  }

  .nav-link:hover {
    color: var(--fg);
  }

  .nav-link:hover::after {
    width: 100%;
  }

  .admin-link {
    font-size: 0.9rem;
  }

  @media (max-width: 600px) {
    .nav {
      padding: 0.75rem 1rem;
    }

    .logo {
      font-size: 1.25rem;
    }

    .nav-links {
      gap: 1.25rem;
    }
  }

  .main {
    flex: 1;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
    width: 100%;
  }

  .footer {
    margin-top: 4rem;
    padding: 2rem 1.5rem;
    text-align: center;
    color: var(--fg-muted);
    font-size: 0.9rem;
    border-top: 1px solid var(--border);
  }
</style>
