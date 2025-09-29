import "./Home.css";

export default function Home() {
  return (
    <div className="home-page">
      <header className="home-header">
        <div className="home-brand" aria-label="品牌与模型选择">
          <span className="home-brand__name">IntuiPilot</span>
          <button className="home-brand__model" type="button">
            <span className="home-brand__model-label">5 Thinking</span>
            <svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">
              <path
                d="M4.47 6.03a.75.75 0 0 1 1.06 0L8 9.5l2.47-3.47a.75.75 0 0 1 1.06 1.06l-3 4.2a.75.75 0 0 1-1.06 0l-3-4.2a.75.75 0 0 1 0-1.06Z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>

        <button className="home-settings" type="button" aria-label="设置">
          <svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">
            <path
              d="M16 4l3.48 3.8 4.97-.16-.16 4.97L28 16l-3.72 3.4.16 4.96-4.96-.16L16 28l-3.4-3.72-4.96.16.16-4.96L4 16l3.8-3.48-.16-4.97 4.97.16Z"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <circle cx="16" cy="16" r="4.5" fill="none" stroke="currentColor" strokeWidth="2" />
          </svg>
        </button>
      </header>

      <main className="home-main">
        <div className="home-main__inner">
          <h1 className="home-title">您在忙什么？</h1>

          <section className="home-search" role="group" aria-label="提问输入区">
            <button className="home-icon-button" type="button" aria-label="新增对话">
              <svg viewBox="0 0 20 20" aria-hidden="true" focusable="false">
                <path
                  d="M10 4.25a.75.75 0 0 1 .75.75v4.25H15a.75.75 0 0 1 0 1.5h-4.25V15a.75.75 0 0 1-1.5 0v-4.25H5a.75.75 0 0 1 0-1.5h4.25V5a.75.75 0 0 1 .75-.75Z"
                  fill="currentColor"
                />
              </svg>
            </button>

            <button className="home-pill" type="button">
              <svg viewBox="0 0 20 20" aria-hidden="true" focusable="false">
                <path
                  d="M10 4.5a5.5 5.5 0 0 0-4.89 3.05.75.75 0 0 0 1.33.7A4 4 0 1 1 6 10a3.98 3.98 0 0 1 3-3.86V7a1 1 0 0 0 1.66.75l2.32-1.93a1 1 0 0 0 0-1.5L10.66 2.4A1 1 0 0 0 9 3.15V4.3A5.5 5.5 0 0 0 10 4.5Z"
                  fill="currentColor"
                />
              </svg>
              <span>进阶思考</span>
            </button>

            <span className="home-placeholder">询问任何问题</span>

            <div className="home-actions">
              <button className="home-icon-button" type="button" aria-label="语音输入">
                <svg viewBox="0 0 20 20" aria-hidden="true" focusable="false">
                  <path
                    d="M10 3a2.5 2.5 0 0 0-2.5 2.5v3a2.5 2.5 0 1 0 5 0v-3A2.5 2.5 0 0 0 10 3Zm-5 5.5a.75.75 0 0 0-1.5 0 6.5 6.5 0 0 0 5.75 6.46v1.54H7.5a.75.75 0 0 0 0 1.5h5a.75.75 0 0 0 0-1.5h-1.75V15a6.5 6.5 0 0 0 5.75-6.5.75.75 0 0 0-1.5 0 5 5 0 0 1-10 0Z"
                    fill="currentColor"
                  />
                </svg>
              </button>
              <button className="home-icon-button" type="button" aria-label="录音设置">
                <svg viewBox="0 0 20 20" aria-hidden="true" focusable="false">
                  <path
                    d="M6.75 5.5a.75.75 0 0 1 .75.75v7.5a.75.75 0 0 1-1.5 0v-7.5a.75.75 0 0 1 .75-.75Zm6.5 1.5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5a.75.75 0 0 1 .75-.75Zm-3.25-3a.75.75 0 0 1 .75.75v10.5a.75.75 0 0 1-1.5 0V4.75a.75.75 0 0 1 .75-.75Z"
                    fill="currentColor"
                  />
                </svg>
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
