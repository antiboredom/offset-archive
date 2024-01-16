<script>
  // import offsetData from "../data.json";
  import { onMount, tick } from "svelte";
  import Project from "$lib/Project.svelte";
  export let data;
  let offsetData = [];
  let q = data.q;
  let start = data.start;
  let count = data.count;
  let sortKey = data.sortKey;
  let methodologyFilter = data.methodologyFilter;
  let projectTypeFilter = data.projectTypeFilter;
  let sortOrder = data.sortOrder;
  let methodologies = {};
  let projectTypes = {};
  let form;
  let loading = false;

  async function subForm() {
    start = 0;
    await tick();
    form.requestSubmit();
  }

  function clearForm() {
    q = "";
    start = 0;
    count = 50;
    projectTypeFilter = null;
    methodologyFilter = null;
    sortKey = "name";
    sortOrder = "asc";
  }

  async function nextPage() {
    start += count;
    if (start > total) start = total - count;
    await tick();
    form.requestSubmit();
  }

  async function prevPage() {
    start -= count;
    if (start < 0) start = 0;
    await tick();
    form.requestSubmit();
  }

  onMount(async () => {
    console.log("loading");
    loading = true;
    let _methodologies = {};
    let _projectTypes = {};

    const res = await fetch(`/offset.json`);

    offsetData = await res.json();

    offsetData.forEach((p, i) => {
      p.id = i;
      _methodologies[p.methodology] = _methodologies[p.methodology]
        ? _methodologies[p.methodology] + 1
        : 1;
      _projectTypes[p.project_type] = _projectTypes[p.project_type]
        ? _projectTypes[p.project_type] + 1
        : 1;
    });

    methodologies = _methodologies;
    projectTypes = _projectTypes;

    loading = false;
  });

  // offsetData.forEach((p, i) => {
  //   p.id = i;
  //   methodologies[p.methodology] = methodologies[p.methodology]
  //     ? methodologies[p.methodology] + 1
  //     : 1;
  //   projectTypes[p.project_type] = projectTypes[p.project_type]
  //     ? projectTypes[p.project_type] + 1
  //     : 1;
  // });

  const sortKeys = [
    { key: "name", text: "Name" },
    { key: "total_credits", text: "Total Credits Issued" },
  ];

  $: offsets = [...offsetData]
    .sort((a, b) => {
      const comp = sortOrder === "asc" ? 1 : -1;
      if (a[sortKey] < b[sortKey]) {
        return -1 * comp;
      }
      if (a[sortKey] > b[sortKey]) {
        return 1 * comp;
      }
      return a.id - b.id;
    })
    .filter((p) => {
      if (q == "") {
        return true;
      }

      if (!p.name) p.name = "";

      return (
        p.name.toLowerCase().indexOf(q.toLowerCase()) > -1 ||
        p.description.toLowerCase().indexOf(q.toLowerCase()) > -1
      );
    })
    .filter((p) => {
      if (methodologyFilter === null) return true;

      return p.methodology == methodologyFilter;
    })
    .filter((p) => {
      if (projectTypeFilter === null) return true;

      return p.project_type == projectTypeFilter;
    });

  $: offsetsSlice = offsets.slice(start, start + count);

  $: total = offsets.length;
</script>

<div class="project-container">
  <form class="filters" method="GET" bind:this={form}>
    <div class="filter">
      <input
        type="text"
        placeholder="Search"
        name="q"
        autofocus
        bind:value={q}
        on:keyup={() => {
          start = 0;
          form.requestSubmit();
        }}
      />
    </div>

    <div class="filter">
      <label for="sort">Sort by</label>
      <select name="sort" id="sort" bind:value={sortKey} on:change={subForm}>
        {#each sortKeys as s}
          <option value={s.key}>
            {s.text}
          </option>
        {/each}
      </select>

      <select name="sortOrder" bind:value={sortOrder} on:change={subForm}>
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
    </div>

    <div class="filter">
      <label for="meth">Methodologies</label>
      <select
        name="methodology"
        id="meth"
        bind:value={methodologyFilter}
        class="long-select"
        on:change={subForm}
      >
        <option value={null}>All Methodologies</option>
        {#each Object.keys(methodologies).sort() as m}
          <option value={m}>
            {m} ({methodologies[m]})
          </option>
        {/each}
      </select>
    </div>

    <div class="filter">
      <label for="ptype">Project Type</label>
      <select
        name="projectType"
        id="ptype"
        bind:value={projectTypeFilter}
        class="long-select"
        on:change={subForm}
      >
        <option value={null}>All Project Types</option>
        {#each Object.keys(projectTypes).sort() as t}
          <option value={t}>
            {t} ({projectTypes[t]})
          </option>
        {/each}
      </select>
    </div>

    <div class="filter">
      <button on:click={clearForm}>Reset</button>
      <button type="submit">Apply</button>
    </div>
    <input type="hidden" name="start" bind:value={start} />
  </form>

  <div class="offsets">
    {#if loading}
      <div>Loading...</div>
    {:else}
      <div class="pagination">
        <div class="page-counts">
          {#if total > 0}
            {start + 1} to {start + Math.min(count, total)} of {total}
          {:else}
            No results found.
          {/if}
        </div>
        <div class="page-buttons">
          {#if start > 0}
            <button on:click={prevPage}>Prev</button>
          {/if}
          {#if start + count < total}
            <button on:click={nextPage}>Next</button>
          {/if}
        </div>
      </div>
      <div class="offsets-inner">
        {#each offsetsSlice as offset (offset.id)}
          <Project {offset} {q} />
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .project-container {
    display: grid;
    grid-template-columns: 200px minmax(0, 1fr);
    margin-top: 1rem;
  }
  .filters {
    margin-right: 1rem;
    padding-right: 1rem;
    border-right: 1px solid var(--fg);
  }
  .filter {
    margin-bottom: 1.5rem;
  }
  .offsets {
    min-width: 0;
  }
  .offsets-inner {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
    grid-gap: 1rem;
  }
  label,
  select,
  input,
  button {
    display: block;
    width: 100%;
    padding: 3px;
    margin-top: 5px;
  }
  label {
    padding: 0;
  }
  button[type="submit"] {
    background-color: var(--theme1);
  }

  .pagination {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  .pagination button {
    display: inline-block;
    width: auto;
  }
</style>
