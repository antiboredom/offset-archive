<script>
  import "./styles.css";
  import { page } from "$app/stores";
</script>

<svelte:head>
  <title>Offset Archive</title>
</svelte:head>

<header>
  <a class="logo" href="/"><img src="/logo.gif" alt="Offset logo" />Offset Archive</a>
  <div class="subhead">A repository of carbon offset projects & sales</div>
  <nav>
    <a href="/" class:active={$page.url.pathname === "/"}>Projects</a>
    <a href="/sales" class:active={$page.url.pathname === "/sales"}>Sales</a>
    <!-- <a -->
    <!--   href="/methodologies" -->
    <!--   class:active={$page.url.pathname === "/methodologies"}>Methodologies</a -->
    <!-- > -->
    <a href="/about" class:active={$page.url.pathname === "/about"}>About</a>
  </nav>
</header>

<main>
  <slot />
</main>