import { For, Show, createResource, createSignal } from "solid-js";
import { suggest, type Resume, type Job } from "./api";

export function App() {
  const [resume, setResume] = createSignal<Resume>();
  const [jobs] = createResource(resume, suggest);

  return (
    <div class="container mx-auto p-4">
      <div class="grid sm:grid-cols-2 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-4">jobrouter</h1>
          <p class="text-gray-600 mb-8">Find jobs based on your CV</p>
          <ResumeForm search={setResume} />
        </div>
        <div>
          <Show when={jobs.loading}>
            <Loader />
          </Show>
          <Show when={jobs()}>
            {jobs => <JobList jobs={jobs()} />}
          </Show>
        </div>
      </div>
    </div>
  )
}

function ResumeForm(props: { search: (r: Resume) => void }) {
  function onSubmit(e: SubmitEvent & { currentTarget: HTMLFormElement }) {
    e.preventDefault();
    const resumeText = new FormData(e.currentTarget).get('resume')?.toString();
    resumeText && props.search({ text: resumeText });
  }
  return (
    <form onSubmit={onSubmit}>
      <textarea name="resume" placeholder="Paste your resume" required class="w-full p-2 border border-gray-300 rounded-md"></textarea>
      <button class="bg-red-500 text-white px-4 py-2 rounded-md mt-4 hover:bg-red-600 transition-colors duration-200">Find jobs</button>
    </form>
  );
}

function JobList(props: { jobs: Job[] }) {
  return (
    <ul>
      <For each={props.jobs}>
        {j => <li class="bg-gray-100 p-4 mb-2 rounded-md whitespace-pre-line">{j.text}</li>}
      </For>
    </ul>
  )
}

function Loader() {
  return (
    <div class="flex justify-center items-center text-white">
      <svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM20 12a8 8 0 01-8 8v-4c2.206 0 4.223-.896 5.657-2.343l2.343-2.343zM16.971 4.062A7.962 7.962 0 0120 12h4c0-3.042-1.135-5.824-3-7.938l-3 2.648z"></path>
      </svg>
      <span>Loading...</span>
    </div>
  );
}
