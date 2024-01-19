<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"    // 해시 기반 라우팅을 위한 URL 규칙 등록
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import Navigation from "./components/Navigation.svelte"
  import UserCreate from './routes/UserCreate.svelte'
  import UserLogin from './routes/UserLogin.svelte'
  import QuestionModify from './routes/QuestionModify.svelte'
  import AnswerModify from './routes/AnswerModify.svelte'

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,    // URL 규칙 정의
    '/question-create': QuestionCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>

<Navigation/>
<Router {routes}/>