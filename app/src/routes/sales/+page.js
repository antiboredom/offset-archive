import salesData from "../../sales.json";

const { headers, values } = salesData;

const registries = ["Gold Standard", "Verra", "American Carbon Registry"];

const _sales = values.map((v) => {
  return {
    id: v[0],
    date: v[1],
    notes: v[2] + "",
    total: v[3],
    type: v[4],
  };
});

export async function load({ url }) {
  let start = url.searchParams.get("start") || 0;
  start = +start;
  if (start < 0 || !start) start = 0;

  let count = url.searchParams.get("count") || 50;
  count = +count;
  if (count < 0 || !count) count = 50;

  let sortKey = url.searchParams.get("sort") || "total";
  let sortOrder = url.searchParams.get("sortOrder") || "desc";

  // let methodologyFilter = url.searchParams.get("methodology") || null;
  //
  // let projectTypeFilter = url.searchParams.get("projectType") || null;
  //
  // let registryFilter = url.searchParams.get("registry") || null;

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
  // .filter((p) => {
  //   if (methodologyFilter === null) return true;
  //
  //   return p.methodology == methodologyFilter;
  // })
  // .filter((p) => {
  //   if (projectTypeFilter === null) return true;
  //
  //   return p.project_type == projectTypeFilter;
  // })
  // .filter((p) => {
  //   if (registryFilter === null) return true;
  //
  //   return p.registry == registryFilter;
  // });

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
