import os
import subprocess
import csv
import sys

def get_fasta_header_details(fasta_file):
    """Extracts the accession and description from the FASTA file header."""
    with open(fasta_file, "r") as f:
        first_line = f.readline().strip()
        if first_line.startswith(">"):
            header_content = first_line[1:].strip().split(maxsplit=1)  # Split into accession and description
            accession = header_content[0]
            description = header_content[1] if len(header_content) > 1 else "No description"
            return accession, description
        return "Unknown", "No description"

def run_mash(fasta_folder, output_file):
    # Find all FASTA files in the folder
    fasta_files = [f for f in os.listdir(fasta_folder) if f.endswith(".fasta")]

    # Assign a number to each FASTA file and get the accession and description from the header
    file_mapping = {i: fasta_files[i] for i in range(len(fasta_files))}
    header_mapping = {i: get_fasta_header_details(os.path.join(fasta_folder, fasta_files[i])) for i in range(len(fasta_files))}

    # Prepare the output CSV file
    with open(output_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Accession1", "Description1", "Accession2", "Description2", "Mash_Distance", "P-value", "Shared_Hashes"])

        # Loop through each file and run Mash against every other file
        for i in range(len(fasta_files)):
            for j in range(i+1, len(fasta_files)):  # Only compare unique pairs (i < j)
                file1 = os.path.join(fasta_folder, file_mapping[i])
                file2 = os.path.join(fasta_folder, file_mapping[j])

                # Run Mash command
                mash_command = ["mash", "dist", file1, file2]
                result = subprocess.run(mash_command, stdout=subprocess.PIPE, text=True)

                # Parse Mash output (assuming output format is File1, File2, Distance, P-value, Shared hashes)
                mash_output = result.stdout.strip().split("\t")
                if len(mash_output) < 5:
                    print(f"Error in Mash output for files {file1} and {file2}")
                    continue

                distance, p_value, shared_hashes = mash_output[2], mash_output[3], mash_output[4]

                # Extract accession and description for each sequence
                accession1, description1 = header_mapping[i]
                accession2, description2 = header_mapping[j]

                # Write the accession and description to the CSV
                csv_writer.writerow([accession1, description1, accession2, description2, distance, p_value, shared_hashes])

    print("Mash comparison complete. Results saved to:", output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mash_compare.py <fasta_folder> <output_file>")
        sys.exit(1)

    fasta_folder = sys.argv[1]
    output_file = sys.argv[2]

    # Run the mash comparison
    run_mash(fasta_folder, output_file)
