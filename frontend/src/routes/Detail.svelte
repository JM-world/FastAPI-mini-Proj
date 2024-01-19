<script>
    import fastapi from '../lib/api'
    import Error from '../components/Error.svelte'
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from "moment/min/moment-with-locales"
    moment.locale('ko')

    export let params = {}
    let today = new Date()
    let day = ('0' + today.getDate()).slice(-2)
    let question_id = params.question_id
    let question = {answers:[], voter:[], content: ''}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()  // submit 버튼이 눌릴경우 form이 자동으로 전송되는 것을 방지
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi('post', url, params,
            (json) => {
                content = ''
                error = {detail:[]}
                get_question()
            },
            (err_json) => {     // post_answer 함수 호출 시 오류가 발생하면 실행
                error = err_json
            }
        )
    }

    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            console.log(_question_id)
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/')
                },
                (err_json) => {
                    json = err_json
                }
            )
        }
    }

    function delete_answer(_answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: _answer_id
            }
            fastapi('delete', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    json = err_json
                }
            )
        }
    }    

    function vote_question(_question_id) {
        if(window.confirm('추천하시겠습니까?')) {
            let url = "/api/question/vote"
            let params = {
                question_id: _question_id
            }
            fastapi('post', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    json = err_json
                }
            )
        }
    }

    function vote_answer(_answer_id) {
        if(window.confirm('추천하시겠습니까?')) {
            let url = "/api/answer/vote"
            let params = {
                answer_id: _answer_id
            }
            fastapi('post', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    json = err_json
                }
            )
        }
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <div>
        <h2>{question.subject}</h2>
        <hr>
        <div class="d-flex justify-content-between">
            <div>
                <button class="btn btn-sm btn-outline-success" on:click="{() => vote_question(question.id)}">
                    추천
                    <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
                </button>
                {#if question.user && $username === question.user.username}
                <a use:link href="/question-modify/{question.id}"
                    class="btn btn-sm btn-outline-warning" style="margin-right:5px; margin-left:5px;">수정</a>
                <button class="btn btn-sm btn-outline-danger"
                    on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
            </div>
            <div>
                {#if question.modify_date}
                <div class="badge bg-secondary text-dark p-1 text-start" style="margin-right:5px">
                    수정됨
                </div>
                {/if}
                <div class="badge bg-secondary text-dark p-1 text-start" style="margin-right:5px">
                    {#if moment(question.create_date).format("DD") === day}
                    오늘 | {moment(question.create_date).format("a hh:mm")}
                    {:else}
                    {moment(question.create_date).format("YYYY/MM/DD | a hh:mm")}
                    {/if}
                </div>
                <div class="badge bg-secondary text-dark p-1 text-start" style="margin-right:15px">
                    작성자: {question.user ? question.user.username : ""}
                </div>
            </div>
        </div>
    </div>
    <br>
    <div>{@html marked.parse(question.content)}</div>
    <br><br><hr>    
        
    

    <button class="btn btn-secondary" on:click="{() => {
        push('/')
    }}">목록으로</button>

    <br><br><br>

    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">{@html marked.parse(answer.content)}</div>
            <div class="d-flex justify-content-end">
                {#if answer.modify_date}
                <div class="badge bg-secondary text-dark p-1 text-start" style="margin-right:10px">
                    수정됨
                </div>
                {/if}
                <div class="badge bg-secondary text-dark p-1 text-start" style="margin-right:10px">
                    {#if moment(answer.create_date).format("DD") === day}
                    오늘 | {moment(answer.create_date).format("a hh:mm")}
                    {:else}
                    {moment(answer.create_date).format("YYYY/MM/DD | a hh:mm")}
                    {/if}
                </div>
                <div class="badge bg-secondary text-dark p-1 text-start">
                    작성자: {question.user ? question.user.username : ""}
                </div>
            </div>
            <div class="d-flex justify-content-between" style="margin-top:15px;">
                <div>
                    <button class="btn btn-sm btn-outline-secondary" on:click="{() => vote_answer(answer.id)}">
                        추천
                        <span class="badge rounded-pill bg-secondary">{ answer.voter.length }</span>
                    </button>
                </div>
                <div>
                    {#if answer.user && answer.user.username === $username}
                    <a use:link href="/answer-modify/{answer.id}"
                        class="btn btn-sm btn-outline-warning" style="margin-right:5px">수정</a>
                    <button class="btn btn-sm btn-outline-danger" 
                        on:click={() => delete_answer(answer.id)}>삭제</button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
    {/each}
    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content}
                disabled={$is_login ? "" : "disabled"}
                class="form-control"></textarea>
        </div>
        <input type="submit" value="답변 등록" class="btn btn-warning {$is_login ? '' : 'disabled'}"
        on:click="{post_answer}">
    </form>
</div>