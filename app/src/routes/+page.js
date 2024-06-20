let offsetData;
let loaded = false;
const methodologies = {};
const projectTypes = {};

async function loadData(fetch) {
  if (loaded) {
    return true;
  }

  let response = await fetch("/data.json");
  offsetData = await response.json();

  offsetData.forEach((p, i) => {
    p.id = i;

    if (!p.name) p.name = "No Name";
    if (!p.description) p.description = "No Description";

    const pMethodologies = p.methodology
      ? p.methodology.split(";").map((m) => m.trim())
      : ["Unknown"];
    const pTypes = p.project_type
      ? p.project_type.split(";").map((m) => m.trim())
      : ["Unknown"];

    pMethodologies.forEach((m) => {
      methodologies[m] = methodologies[m] ? methodologies[m] + 1 : 1;
    });

    pTypes.forEach((t) => {
      projectTypes[t] = projectTypes[t] ? projectTypes[t] + 1 : 1;
    });
  });
  loaded = true;
}

export async function load({ url, fetch }) {
  await loadData(fetch);
  let start = url.searchParams.get("start") || 0;
  start = +start;
  if (start < 0 || !start) start = 0;

  let count = url.searchParams.get("count") || 50;
  count = +count;
  if (count < 0 || !count) count = 50;

  let sortKey = url.searchParams.get("sort") || "total_credits";
  let sortOrder = url.searchParams.get("sortOrder") || "desc";

  let methodologyFilter = url.searchParams.get("methodology") || null;

  let projectTypeFilter = url.searchParams.get("projectType") || null;

  let registryFilter = url.searchParams.get("registry") || null;

  let q = url.searchParams.get("q") || "";

  const offsets = [...offsetData]
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

      return (
        p.registry_id == q ||
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
    })
    .filter((p) => {
      if (registryFilter === null) return true;

      return p.registry == registryFilter;
    });

  const offsetsSlice = offsets.slice(start, start + count);

  return {
    total: offsets.length,
    offsetsSlice,
    start,
    count,
    q,
    sortKey,
    methodologyFilter,
    projectTypeFilter,
    registryFilter,
    methodologies,
    projectTypes,
    sortOrder,
  };
}
