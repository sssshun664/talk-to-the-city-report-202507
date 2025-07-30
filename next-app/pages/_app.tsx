import { AppProps } from "next/app"
import Head from 'next/head'
import '../globals.css'

export default function App(
  props: AppProps
) {
  const { Component, pageProps } = props
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="format-detection" content="telephone=no" />
        <title>Talk to the City レポート</title>
      </Head>
      <Component {...pageProps} />
    </>
  )
}
