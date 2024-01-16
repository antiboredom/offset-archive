export async function load({ url }) {
  let start = url.searchParams.get("start") || 0;
  start = +start;
  if (start < 0 || !start) start = 0;

  let count = url.searchParams.get("count") || 50;
  count = +count;
  if (count < 0 || !count) count = 50;

  let sortKey = url.searchParams.get("sort") || "name";
  let sortOrder = url.searchParams.get("sortOrder") || "asc";

  let methodologyFilter = url.searchParams.get("methodology") || null;

  let projectTypeFilter = url.searchParams.get("projectType") || null;

  let q = url.searchParams.get("q") || "";

  // let offsets = offsetData
  //   .filter((p) => {
  //     if (q == "") {
  //       return true;
  //     }
  //
  //     if (!p.name) p.name = "";
  //
  //     return (
  //       p.name.toLowerCase().indexOf(q.toLowerCase()) > -1 ||
  //       p.description.toLowerCase().indexOf(q.toLowerCase()) > -1
  //     );
  //   })
  //   .slice(start, start + count);
  // let total = offsets.length;
  // if (!q) total = offsetData.length;

  // return { start, count, q, offsets, total };
  return {
    start,
    count,
    q,
    sortKey,
    methodologyFilter,
    sortOrder,
    projectTypeFilter,
  };
}
