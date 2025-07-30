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
  
  return <div className='mt-6 pb-8'>
    <Outline clusters={clusters} translator={{...translator, t}} />
    <Header {...props} translator={{...translator, t}} />
    
    <div className='content-container'
      style={{ display: openMap ? 'none' : 'block' }}>
      
      {/* メインタイトル */}
      <div className="text-center mb-8">
        <h2 className='text-xl my-3 font-bold text-gray-800'>{t(config.name)}</h2>
        <h1 className='text-3xl my-3 mb-6 font-semibold text-gray-900'>{t(config.question)}</h1>
      </div>

      {/* イントロダクション */}
      <div id="introduction" className='mb-8'>
        {config.intro && (
          <div className='content-card markdown-content' 
               dangerouslySetInnerHTML={{
                 __html: converter.makeHtml(t(config.intro) || '')
               }} />
        )}
        
        {/* メインマップセクション */}
        <div className="content-card text-center">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">�� データ可視化マップ</h3>
          <div className="map-container">
            <Map {...props} translator={{...translator, t}} color={color} width={450} height={450} />
          </div>
          <button 
            className="mobile-button mt-4 underline"
            onClick={() => {
              if (isTouchDevice()) {
                alert('インタラクティブマップはタッチデバイスではまだ利用できません。デスクトップコンピューターからお試しください。')
              } else {
                scroll.current = window.scrollY
                setOpenMap("main")
              }
            }}>
            {t("Open full-screen map")}
          </button>
        </div>
        
        {/* 概要セクション */}
        <div className="content-card">
          <h3 className='text-xl font-bold mb-4 text-gray-800 border-b-2 border-gray-200 pb-2'>
            📋 {t("Overview")}
          </h3>
          <div className='markdown-content' 
               dangerouslySetInnerHTML={{
                 __html: converter.makeHtml(t(overview) || '')
               }} />
        </div>
      </div>
      
      {/* クラスター分析セクション */}
      <div id="clusters">
        <h2 className="text-2xl font-bold text-center mb-6 text-gray-900">
          🎯 クラスター別詳細分析
        </h2>
        
        {clusters.sort((c1, c2) => c2.arguments.length - c1.arguments.length)
          .map((cluster, index) => (
            <div key={cluster.cluster_id} 
                 id={`cluster-${cluster.cluster_id}`} 
                 className="cluster-section"
                 style={{ borderLeftColor: color(cluster.cluster_id) }}>
              
              {/* クラスタータイトル */}
              <h2 className="text-2xl font-semibold mb-3"
                  style={{ color: color(cluster.cluster_id) }}>
                {`${index + 1}. ${t(cluster.cluster)}`}
              </h2>
              
              {/* 統計情報 */}
              <div className="stats-text mb-4">
                💬 {cluster.arguments.length} {t("arguments")} | 
                📊 全体の {Math.round(100 * cluster.arguments.length / totalArgs)}%
              </div>
              
              {/* クラスター分析 */}
              <div className="mb-6">
                <h4 className='text-lg font-bold mb-3 text-gray-800'>
                  🔍 {t("Cluster analysis")}
                </h4>
                <div className='markdown-content'
                     dangerouslySetInnerHTML={{
                       __html: converter.makeHtml(t(cluster.takeaways) || '')
                     }} />
              </div>
              
              {/* クラスターマップ */}
              <div className='text-center mb-6'>
                <h4 className='text-lg font-bold mb-3 text-gray-800'>
                  🗺️ このクラスターの分布
                </h4>
                <div className="cluster-map">
                  <Map {...props} 
                       translator={{...translator, t}} 
                       color={color} 
                       width={350} 
                       height={350} 
                       onlyCluster={t(cluster.cluster_id)} />
                </div>
                <button 
                  className="mobile-button mt-3 underline" 
                  onClick={() => {
                    if (isTouchDevice()) {
                      alert('インタラクティブマップはタッチデバイスではまだ利用できません。デスクトップコンピューターからお試しください。')
                    } else {
                      scroll.current = window.scrollY
                      setOpenMap(cluster.cluster_id)
                    }
                  }}>
                  {t("Open full-screen map")}
                </button>
              </div>
              
              {/* 代表的なコメント */}
              <div>
                <h4 className='text-lg font-bold mb-3 text-gray-800'>
                  💭 {t("Representative comments")}
                </h4>
                <div className='representative-comments'>
                  <ul className='space-y-2'>
                    {cluster.arguments
                      .sort((a, b) => b.p - a.p)
                      .slice(0, 5)
                      .map((arg, i) => (
                        <li key={i} className='italic text-gray-700'>
                          "{t(arg.argument)}"
                        </li>
                      ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
      </div>
      
      <Appendix config={config} translator={{...translator, t}} />
    </div>
  </div>
}

export default Report
