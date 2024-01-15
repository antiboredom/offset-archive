<script>
  import { goto } from "$app/navigation";
  import offsetData from "../data.json";
  import Project from "$lib/Project.svelte";
  export let data;
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

  function subForm() {
    form.requestSubmit();
  }

  function clearForm() {
    q = "";
    start = 0;
    count = 100;
    projectTypeFilter = null;
    methodologyFilter = null;
    sortKey = "name";
    sortOrder = "asc";
  }

  offsetData.forEach((p, i) => {
    p.id = i;
    methodologies[p.methodology] = methodologies[p.methodology]
      ? methodologies[p.methodology] + 1
      : 1;
    projectTypes[p.project_type] = projectTypes[p.project_type]
      ? projectTypes[p.project_type] + 1
      : 1;
  });

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

  // console.log(offsets.length)

  $: total = offsets.length;

  console.log(total);
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
        on:keyup={() => form.requestSubmit()}
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
      <button on:click={clearForm}>Clear</button>
      <button type="submit">Apply</button>
    </div>
  </form>

  <div class="offsets">
    <p>{start + 1} to {start + Math.min(count, total)} of {total}</p>
    <div class="offsets-inner">
      {#each offsetsSlice as offset (offset.id)}
        <Project {offset} {q} />
      {/each}
    </div>
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
</style>
