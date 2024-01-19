<script>
  import fastapi from "../lib/api"
  import { link } from 'svelte-spa-router'
  import { page, keyword, is_login } from "../lib/store"
  import moment from "moment/min/moment-with-locales"
  moment.locale('ko')

  // 초기값을 주지 않으면 fetch 함수는 비동기 방식으로 실행되므로
  // HTML 영역의 question_list에 값이 없어서 오류가 출력된다.
  let question_list = []

  // 8000으로 접속시 콘솔창에 detail not found 해결을 위한 코드
  let detail = {detail: []}

  let today = new Date();
  let day = ('0' + today.getDate()).slice(-2)
  let size = 10
  let total = 0
  let kw = ''
  $: total_page = Math.ceil(total/size)

  function get_question_list() {
    let params = {
      page: $page,
      size: size,
      keyword: $keyword,
    }
    fastapi('get', '/api/question/list', params, (json) => {
      question_list = json.question_list
      total = json.total
      kw = $keyword
    })
  }

  $:$page, $keyword, get_question_list($page)
</script>

<div class="container my-3">
  <div class="row my-3">
    <div class="col-6">
      <a use:link href="/question-create"
        class="btn btn-warning {$is_login ? '' : 'disabled'}">질문 등록하기</a> 
    </div>
    <div class="col-6">
      <div class="input-group">
        <a use:link class="btn btn-outline-secondary" href="/" 
            on:click="{() => {$keyword = '', $page = 0}}">초기화</a>
        <input type="text" class="form-control" placeholder="ex) 제목, 댓글, 닉네임" bind:value="{kw}">
        <button class="btn btn-outline-warning" on:click={() => {$keyword = kw, $page = 0}}>
          찾기
        </button>
      </div>
    </div>
  </div>
  <table class="table">
    <thead>
    <tr class="text-center table-warning">
      <th>번호</th>
      <th style="width:50%">제목</th>
      <th>작성자</th>
      <th>작성일시</th>
    </tr>
    </thead>
    <tbody>
    {#each question_list as question, i}
    <tr class="text-center">
      <td>{total - ($page * size) - i}</td>
      <td class="text-start">
        <a use:link href="/detail/{question.id}">{question.subject}</a>
        {#if question.answers.length > 0}
        <span class="text-danger small mx-2">&#91;{question.answers.length}&#93;</span>
        {/if}
      </td>
      <td>{ question.user ? question.user.username: ""}</td>
      {#if moment(question.create_date).format("DD") === day}
      <td>{moment(question.create_date).format("a hh:mm")}</td>
      {:else}
      <td>{moment(question.create_date).format("MM/DD")}</td>
      {/if}
    </tr>
    {/each}
    </tbody>
  </table>
  <!-- 페이징 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 첫 페이지로 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click="{() => $page = 0}">&lt;&lt;</button>
    </li>
    <!-- 이전 페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      {#if $page <= 4}
      <button class="page-link" on:click="{() => $page = 0}">&lt;</button>
      {:else if $page > 4}
      <button class="page-link" on:click="{() => $page -= 5}">&lt;</button>
      {/if}
    </li>
    <!-- 페이지 번호 -->
    {#each Array(total_page) as _, loop_page}
    <li class="page-item {loop_page === $page && 'active'}">
      {#if $page === 0 && loop_page <= $page+4}
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      {:else if $page === 1 && loop_page >= $page-1 &&loop_page <= $page+3}
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      {:else if $page === total_page -1 && loop_page >= $page-4}
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      {:else if $page === total_page -2 && loop_page >= $page-3}
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      {:else if loop_page >= $page-2 && loop_page <= $page+2}
      <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      {/if}
    </li>
    {/each}
    <!-- 다음 페이지 -->
    <li class="page-item {$page >= total_page-1 && 'disabled'}">
      {#if $page >= total_page -5}
      <button class="page-link" on:click="{() => $page = total_page-1}">&gt;</button>
      {:else if $page < total_page -5}
      <button class="page-link" on:click="{() => $page += 5}">&gt;</button>
      {/if}
    </li>
    <!-- 끝 페이지로 -->
    <li class="page-item {$page >= total_page-1 && 'disabled'}">
      <button class="page-link" on:click="{() => $page = total_page-1}">&gt;&gt;</button>
    </li>
  </ul>
  <!-- 페이징 처리 끝 -->
</div>