export type Resume = { text: string };
export type Job = { text: string };
export type JobSuggest = Job[];

async function safeFetch(...args: Parameters<typeof fetch>) {
  const res = await fetch(...args);
  if (!res.ok) {
    throw new Error();
  }
  return res;
}

export async function suggest(resume: Resume): Promise<JobSuggest> {
  const body = JSON.stringify(resume);
  const res = await safeFetch('/suggest', { 
    method: 'POST', 
    body, 
    headers: { 'content-type': 'application/json' }
  });
  return res.json();
}
