import React, { useState, useEffect, use, useRef } from 'react';
import { Result, Point } from '@/types';
import useClusterColor from '@/hooks/useClusterColor';
import useTranslatorAndReplacements from '@/hooks/useTranslatorAndReplacements';
import Map from './Map';
import Header from './Header';
import Appendix from './Appendix';
import Outline from './Outline';
import { isTouchDevice } from '@/utils';
import showdown from 'showdown';

type ReportProps = Result
const converter = new showdown.Converter();

// 日本語UIラベル定数
const JA_LABELS: { [key: string]: string } = {
  "Open full-screen map": "フルスクリーンマップを開く",
  "Overview": "概要",
  "arguments": "個の議論",
  "of total": "（全体の",
  "Cluster analysis": "クラスター分析",
  "Representative comments": "代表的なコメント",
  "Introduction": "はじめに",
  "Clusters": "クラスター",
  "Appendix": "付録",
  "Back to report": "レポートに戻る",
  "Hide labels": "ラベルを隠す",
  "Show labels": "ラベルを表示",
  "Show filters": "フィルターを表示",
  "Hide filters": "フィルターを隠す",
  "Min. votes": "最小投票数",
  "Consensus": "合意度",
  "Showing": "表示中",
  "Reset zoom": "ズームをリセット",
  "Click anywhere on the map to close this": "マップのどこかをクリックして閉じる",
  "Click on the dot for details": "詳細を見るには点をクリック",
  "agree": "賛成",
  "disagree": "反対",
  "Language": "言語",
  "English": "英語",
  "%)": "%）"
};

function Report(props: ReportProps) {

  const [openMap, setOpenMap] = useState<string | null>(null)
  const { config, clusters, translations, overview } = props
  const color = useClusterColor(clusters.map(c => c.cluster_id))
  const scroll = useRef(0)
  const translator = useTranslatorAndReplacements(config, translations, clusters)

  // wait for one tick to avoid SSR issues
  const [ready, setReady] = useState(false)
  useEffect(() => { setReady(true) }, [])
  if (!ready) return false

  // 日本語対応のt関数（型を元の関数に合わせる）
  const { t: originalT } = translator
  const t = (txt?: string): string | undefined => {
    if (!txt) return txt;
    // まず日本語ラベルをチェック
    if (JA_LABELS[txt]) {
      return JA_LABELS[txt];
    }
    // 翻訳が設定されている場合は元のt関数を使用
    return originalT(txt);
  }

  const totalArgs = clusters.map(c => c.arguments.length).reduce((a, b) => a + b, 0)

  if (openMap) {
    return <Map {...props} color={color} translator={{...translator, t}} back={() => {
      setOpenMap(null)
      setTimeout(() => window.scrollTo({ top: scroll.current }), 0)
    }} fullScreen onlyCluster={openMap !== 'main' ? openMap : undefined} />
  }
  return <div className='mt-9'>
    <Outline clusters={clusters} translator={{...translator, t}} />
    <Header {...props} translator={{...translator, t}} />
    <div className='text-center max-w-3xl m-auto py-8 px-5'
      style={{ display: openMap ? 'none' : 'block' }}>
      <h2 className='text-xl my-3 font-bold'>{t(config.name)}</h2>
      <h1 className='text-3xl my-3 mb-10'>{t(config.question)}</h1>

      <div id="introduction" className='my-4'>
        {config.intro &&
          <div className='max-w-xl m-auto mb-4 text-justify italic' dangerouslySetInnerHTML={{
            __html: converter.makeHtml(t(config.intro) || '')
          }} />}
        <div id="big-map">
          <Map {...props} translator={{...translator, t}} color={color} width={450} height={450} />
          <button className="my-2 underline"
            onClick={() => {
              if (isTouchDevice()) {
                alert('インタラクティブマップはタッチデバイスではまだ利用できません。デスクトップコンピューターからお試しください。')
              } else {
                scroll.current = window.scrollY
                setOpenMap("main")
              }
            }}>
            {t("Open full-screen map")}</button>
        </div>
        <div id="overview" className='text-left font-bold my-3'>{t("Overview")}:</div>
        <div className='text-left'>{t(overview)}</div>
      </div>
      <div id="clusters">
        {clusters.sort((c1, c2) => c2.arguments.length - c1.arguments.length)
          .map((cluster) => <div key={cluster.cluster_id} id={`cluster-${cluster.cluster_id}`}>
            <h2 className="text-2xl font-semibold my-2 mt-12"
              style={{ color: color(cluster.cluster_id) }}>{t(cluster.cluster)}</h2>
            <div className="text-lg opacity-50 mb-3">({cluster.arguments.length} {t("arguments")}、
              {Math.round(100 * cluster.arguments.length / totalArgs)}% {t("of total")}{t("%)}")}</div>
            <div className='text-left font-bold my-3'>{t("Cluster analysis")}:</div>
            <div className='text-left'>{t(cluster.takeaways)}</div>
            <div className='my-4'>
              <Map  {...props} translator={{...translator, t}} color={color} width={350} height={350} onlyCluster={t(cluster.cluster_id)} />
              <button className="my-2 underline" onClick={() => {
                if (isTouchDevice()) {
                  alert('インタラクティブマップはタッチデバイスではまだ利用できません。デスクトップコンピューターからお試しください。')
                } else {
                  scroll.current = window.scrollY
                  setOpenMap(cluster.cluster_id)
                }
              }}>{t("Open full-screen map")}</button>
            </div>
            <div className='text-left font-bold my-3'>{t("Representative comments")}:</div>
            <ul className='text-left list-outside list-disc ml-6 '>
              {cluster.arguments
                .sort((a, b) => b.p - a.p)
                .slice(0, 5).map((arg, i) =>
                  <li key={i} className='italic'>{t(arg.argument)}</li>
                )}
            </ul>
          </div>)}
      </div>
      <Appendix config={config} translator={{...translator, t}} />
    </div>
  </div>
}

export default Report
