<script>
  import { tick } from "svelte";
  export let data;

  let q = data.q;
  let start = data.start;
  let count = data.count;
  let sortKey = data.sortKey;
  let sortOrder = data.sortOrder;
  let form;

  const sortKeys = [
    { key: "notes", text: "Notes" },
    { key: "total", text: "Total Credits" },
    { key: "date", text: "Date" },
  ];

  $: salesSlice = data.salesSlice;
  $: total = data.total;

  async function subForm() {
    start = 0;
    await tick();
    form.requestSubmit();
  }

  function clearForm() {
    q = "";
    start = 0;
    count = 50;
    sortKey = "total";
    sortOrder = "desc";
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
</script>

<div class="project-container">
  <form class="filters" method="GET" action="/sales" bind:this={form}>
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
      <button class="reset" on:click={clearForm}>Reset</button>
      <!-- <button type="submit">Apply</button> -->
    </div>
    <input type="hidden" name="start" bind:value={start} />
  </form>

  <div>
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
    <table>
      <tr>
        <th>Project ID</th>
        <th>Total</th>
        <th>Date</th>
        <th>Notes</th>
      </tr>
      {#each salesSlice as sale}
        <tr>
          <td>{sale.id}</td>
          <td>{sale.total.toLocaleString()}</td>
          <td>{sale.date}</td>
          <td>{sale.notes}</td>
        </tr>
      {/each}
    </table>
  </div>
</div>

<style>
  table {
    border-collapse: collapse;
    width: 100%;
  }
  th {
    font-weight: normal;
    text-align: left;
  }
  td,
  th {
    border-bottom: 1px solid #000;
    padding: 10px;
    vertical-align: top;
  }
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
  .reset {
    background-color: #eee;
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
  @media (max-width: 768px) {
    .project-container {
      display: grid;
      grid-template-columns: 100%;
      margin-top: 1rem;
    }
    .filters {
      margin-right: 0;
      padding-right: 0;
      border-right: none;
    }
  }
</style>
