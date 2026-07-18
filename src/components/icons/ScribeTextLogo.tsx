const ScribeTextLogo = ({
  width,
  height,
  className,
}: {
  width?: number | string;
  height?: number | string;
  className?: string;
}) => {
  // Horizontal lockup: waveform mark + wordmark. The viewBox keeps the
  // original logo's ~2.84:1 ratio so existing call sites lay out unchanged.
  const bars = [0.35, 0.7, 1.0, 0.7, 0.35];
  const barW = 20;
  const gap = 14;
  const maxH = 150;
  const cy = 112.5;

  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 640 225"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {bars.map((ratio, i) => {
        const h = maxH * ratio;
        return (
          <rect
            key={i}
            className="logo-primary"
            x={10 + i * (barW + gap)}
            y={cy - h / 2}
            width={barW}
            height={h}
            rx={barW / 2}
          />
        );
      })}
      <text
        className="logo-stroke"
        x={210}
        y={cy}
        dominantBaseline="central"
        fontFamily="system-ui, -apple-system, 'Segoe UI', sans-serif"
        fontSize={132}
        fontWeight={600}
        letterSpacing={-2}
        strokeWidth={0}
      >
        Scribe
      </text>
    </svg>
  );
};

export default ScribeTextLogo;
