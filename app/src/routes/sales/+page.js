const registries = ["Gold Standard", "Verra", "American Carbon Registry"];

let salesData;
let headers;
let values;
let _sales;
let loaded = false;

async function loadData(fetch) {
  if (!loaded) {
    let response = await fetch("/sales.json");
    salesData = await response.json();
    headers = salesData.headers;
    values = salesData.values;

    _sales = values.map((v) => {
      return {
        id: v[0],
        date: v[1],
        notes: v[2] + "",
        total: v[3],
        type: v[4],
      };
    });
    loaded = true;
  }
}

export async function load({ url, fetch }) {
  await loadData(fetch);

  let start = url.searchParams.get("start") || 0;
  start = +start;
  if (start < 0 || !start) start = 0;

  let count = url.searchParams.get("count") || 50;
  count = +count;
  if (count < 0 || !count) count = 50;

  let sortKey = url.searchParams.get("sort") || "total";
  let sortOrder = url.searchParams.get("sortOrder") || "desc";

  let q = url.searchParams.get("q") || "";

  const sales = [..._sales]
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
      return p.id == q || p.notes.toLowerCase().indexOf(q.toLowerCase()) > -1;
    });

  const salesSlice = sales.slice(start, start + count);

  return {
    total: sales.length,
    salesSlice,
    start,
    count,
    q,
    sortKey,
    sortOrder,
  };
}
