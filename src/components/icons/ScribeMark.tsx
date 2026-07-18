const ScribeMark = ({
  width,
  height,
}: {
  width?: number | string;
  height?: number | string;
}) => {
  // 5-bar waveform, matching the app icon. Ratios of the max bar height.
  const bars = [0.35, 0.7, 1.0, 0.7, 0.35];
  const barW = 14;
  const gap = 10;
  const maxH = 100;
  const cy = 67.5;
  const startX = (126 - (bars.length * barW + (bars.length - 1) * gap)) / 2;

  return (
    <svg
      width={width || 126}
      height={height || 135}
      viewBox="0 0 126 135"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {bars.map((ratio, i) => {
        const h = maxH * ratio;
        return (
          <rect
            key={i}
            className="logo-primary"
            x={startX + i * (barW + gap)}
            y={cy - h / 2}
            width={barW}
            height={h}
            rx={barW / 2}
          />
        );
      })}
    </svg>
  );
};

export default ScribeMark;
