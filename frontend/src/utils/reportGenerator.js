import jsPDF from "jspdf";
import "jspdf-autotable";

export const generatePDFReport = (data) => {
  const doc = new jsPDF();

  doc.setFontSize(20);
  doc.setTextColor(102, 126, 234);
  doc.text("Smart Job Placement Report", 105, 20, { align: "center" });

  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Generated: ${new Date().toLocaleDateString()}`, 105, 28, { align: "center" });

  doc.setFontSize(14);
  doc.setTextColor(0);
  doc.text("Key Metrics", 20, 45);

  const metricsData = [
    ["Match Score", `${data.gap_analysis.match_score}%`],
    ["Skill Coverage", `${data.gap_analysis.skill_coverage}%`],
    ["Placement Probability", `${data.placement_probability.probability}%`],
    ["Confidence Level", data.placement_probability.confidence]
  ];

  doc.autoTable({ startY: 50, head: [["Metric", "Value"]], body: metricsData, theme: "grid", headStyles: { fillColor: [102, 126, 234] } });

  let currentY = doc.lastAutoTable.finalY + 15;
  doc.text("Matched Skills", 20, currentY);
  doc.autoTable({ startY: currentY + 5, body: [[data.gap_analysis.matched_skills.join(", ")]], theme: "plain", styles: { fillColor: [212, 237, 218] } });

  currentY = doc.lastAutoTable.finalY + 10;
  doc.text("Skills to Develop", 20, currentY);
  doc.autoTable({ startY: currentY + 5, body: [[data.gap_analysis.missing_skills.join(", ")]], theme: "plain", styles: { fillColor: [248, 215, 218] } });

  if (data.recommendations?.courses) {
    doc.addPage();
    doc.text("Recommended Learning Path", 20, 20);
    const courseData = data.recommendations.courses.map(rec => [rec.skill, rec.course, rec.provider, rec.duration]);
    doc.autoTable({ startY: 25, head: [["Skill", "Course", "Provider", "Duration"]], body: courseData, theme: "striped", headStyles: { fillColor: [102, 126, 234] } });
  }

  doc.save("skill-gap-report.pdf");
};
