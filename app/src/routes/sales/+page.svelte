<script>
  import { tick } from "svelte";
  export let data;

  let q = data.q;
  let start = data.start;
  let count = data.count;
  let sortKey = data.sortKey;
  let sortOrder = data.sortOrder;
  let shouldAutoFocus = false;
  let form;

  const URLS = [
    "https://registry.goldstandard.org/projects/details/",
    "https://registry.verra.org/app/projectDetail/VCS/",
    "https://acr2.apx.com/mymodule/reg/prjView.asp?id1=",
    "https://thereserve2.apx.com/mymodule/reg/prjView.asp?id1=",
  ];

  // const REGS = ["Gold", "Verra", "ACR"];

  const sortKeys = [
    { key: "notes", text: "Buyer Information" },
    { key: "total", text: "Total Carbon Credits" },
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

  function getURL(id, type) {
    if (type == 2) {
      id = id.replace("ACR", "");
    }
    if (type == 3) {
      id = id.replace("CAR", "");
    }
    return URLS[type] + id;
  }
</script>

<div class="project-container">
  <form class="filters" method="GET" action="/sales" bind:this={form}>
    <div class="help">
      Offset sales data has been sourced from The Berkeley Carbon Trading
      Project. This dataset consists of the name of every organisation or
      individual who has bought an offset, date of the sale, quantity of offsets
      purchased and from which project.
    </div>
    <div class="filter">
      <input
        type="text"
        placeholder="Search"
        name="q"
        autofocus={shouldAutoFocus}
        bind:value={q}
        on:keyup={() => {
          start = 0;
          form.requestSubmit();
          shouldAutoFocus = true;
        }}
        on:blur={() => {
          shouldAutoFocus = false;
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
        <th width="10%">Project ID</th>
        <!-- <th>Registry</th> -->
        <th width="10%">Carbon Credits</th>
        <th width="10%">Date</th>
        <th>Buyer Information</th>
      </tr>
      {#each salesSlice as sale}
        <tr>
          <td
            ><a target="_blank" href={getURL(sale.id, sale.type)}>{sale.id}</a
            ></td
          >
          <!-- <td>{REGS[sale.type]}</td> -->
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
  th {
    /* white-space: nowrap; */
  }
  td {
    overflow-wrap: anywhere;
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
  .filter,
  .help {
    margin-bottom: 1.5rem;
  }
  .help {
    font-size: 0.9em;
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
